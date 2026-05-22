import re
import wave
from pathlib import Path
from typing import Any

import numpy as np


_INVALID_FILENAME_CHARS = re.compile(r'[/\\:*?"<>|]+')


def _to_numpy(value: Any) -> np.ndarray:
    if isinstance(value, np.ndarray):
        return value

    if hasattr(value, "detach") and hasattr(value, "cpu") and hasattr(value, "numpy"):
        return value.detach().cpu().numpy()

    raise TypeError(
        f"Unsupported audio input type: {type(value)}. "
        "Expected dict with 'waveform', torch.Tensor, or numpy.ndarray."
    )


def _as_samples_channels(waveform: np.ndarray) -> np.ndarray:
    array = np.asarray(waveform)

    if array.ndim == 1:
        return array[:, np.newaxis]

    if array.ndim == 2:
        first, second = array.shape
        if first <= 8 and first <= second:
            return array.T
        return array

    if array.ndim == 3:
        if array.shape[0] < 1:
            raise ValueError(f"Unsupported waveform shape: {array.shape}. Batch dimension is empty.")
        # Initial implementation saves the first batch item. This can be extended to save each batch separately.
        return _as_samples_channels(array[0])

    raise ValueError(
        f"Unsupported waveform shape: {array.shape}. "
        "Expected [samples], [channels, samples], or [batch, channels, samples]."
    )


def prepare_audio_array(audio: Any, fallback_sample_rate: int, normalize: bool) -> tuple[np.ndarray, int]:
    sample_rate = fallback_sample_rate
    waveform = audio

    if isinstance(audio, dict):
        if "waveform" not in audio:
            raise TypeError(
                f"Unsupported audio input type: {type(audio)}. "
                "Expected dict with 'waveform', torch.Tensor, or numpy.ndarray."
            )
        waveform = audio["waveform"]
        sample_rate = int(audio.get("sample_rate") or fallback_sample_rate)

    audio_array = _as_samples_channels(_to_numpy(waveform)).astype(np.float32, copy=False)

    if audio_array.size == 0:
        raise ValueError("Audio waveform is empty.")

    if normalize:
        peak = float(np.max(np.abs(audio_array)))
        if peak > 0.0:
            audio_array = audio_array / peak

    return np.clip(audio_array, -1.0, 1.0), sample_rate


def _safe_filename_prefix(filename_prefix: str) -> str:
    name = _INVALID_FILENAME_CHARS.sub("_", filename_prefix).strip(" ._")
    return name or "audio_output"


def _get_output_directory() -> Path:
    try:
        import folder_paths

        return Path(folder_paths.get_output_directory())
    except ImportError:
        return Path.cwd() / "output"


def _next_numbered_stem(output_dir: Path, prefix: str, extensions: list[str]) -> str:
    index = 1
    while True:
        stem = f"{prefix}_{index:05d}"
        if not any((output_dir / f"{stem}.{extension}").exists() for extension in extensions):
            return stem
        index += 1


def _to_pcm_int16(audio_array: np.ndarray) -> np.ndarray:
    pcm = np.clip(audio_array, -1.0, 1.0)
    return np.ascontiguousarray((pcm * 32767).astype(np.int16))


def _save_wav(path: Path, audio_array: np.ndarray, sample_rate: int) -> None:
    pcm_int16 = _to_pcm_int16(audio_array)
    channels = pcm_int16.shape[1]

    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_int16.tobytes())


def _audio_segment_from_array(audio_array: np.ndarray, sample_rate: int):
    try:
        from pydub import AudioSegment
    except Exception as exc:
        raise RuntimeError(
            "MP3/OGG export requires pydub and ffmpeg. Please install ffmpeg or disable save_mp3/save_ogg."
        ) from exc

    pcm_int16 = _to_pcm_int16(audio_array)
    channels = pcm_int16.shape[1]
    return AudioSegment(
        pcm_int16.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=channels,
    )


def _save_with_pydub(path: Path, audio_array: np.ndarray, sample_rate: int, file_format: str) -> None:
    segment = _audio_segment_from_array(audio_array, sample_rate)

    try:
        segment.export(str(path), format=file_format.lower())
    except Exception as exc:
        raise RuntimeError(
            f"{file_format} export requires ffmpeg. Please install ffmpeg or disable save_{file_format.lower()}."
        ) from exc


class AudioMultiFormatSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "filename_prefix": ("STRING", {"default": "audio_output"}),
                "save_wav": ("BOOLEAN", {"default": True}),
                "save_mp3": ("BOOLEAN", {"default": False}),
                "save_ogg": ("BOOLEAN", {"default": False}),
                "sample_rate": ("INT", {"default": 44100, "min": 8000, "max": 192000, "step": 1}),
                "normalize": ("BOOLEAN", {"default": False}),
                "overwrite": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("saved_files",)
    FUNCTION = "save_audio"
    CATEGORY = "RyoheiTanaka/Audio"
    OUTPUT_NODE = True

    def save_audio(
        self,
        audio,
        filename_prefix="audio_output",
        save_wav=True,
        save_mp3=False,
        save_ogg=False,
        sample_rate=44100,
        normalize=False,
        overwrite=False,
    ):
        enabled_formats = []
        if save_wav:
            enabled_formats.append("wav")
        if save_mp3:
            enabled_formats.append("mp3")
        if save_ogg:
            enabled_formats.append("ogg")

        if not enabled_formats:
            raise ValueError("At least one output format must be enabled: save_wav, save_mp3, or save_ogg.")

        audio_array, effective_sample_rate = prepare_audio_array(audio, sample_rate, normalize)
        output_dir = _get_output_directory()
        output_dir.mkdir(parents=True, exist_ok=True)

        safe_prefix = _safe_filename_prefix(filename_prefix)
        stem = safe_prefix if overwrite else _next_numbered_stem(output_dir, safe_prefix, enabled_formats)

        saved_files = []
        for extension in enabled_formats:
            path = output_dir / f"{stem}.{extension}"
            if extension == "wav":
                _save_wav(path, audio_array, effective_sample_rate)
            elif extension == "ogg":
                _save_with_pydub(path, audio_array, effective_sample_rate, "OGG")
            elif extension == "mp3":
                _save_with_pydub(path, audio_array, effective_sample_rate, "MP3")
            saved_files.append(str(path))

        return ("Saved files:\n" + "\n".join(saved_files),)
