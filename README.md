# ComfyUI Lab

**学習・実験用の ComfyUI カスタムノード集です。**

このリポジトリは、個人の学習と実験を目的とした ComfyUI 向けカスタムノードをまとめたものです。
動作は保証されていないため、使用は自己責任でお願いします。

---

## Audio Multi Format Saver

`Audio Multi Format Saver` は、ComfyUI 上の音声データを WAV / MP3 / OGG 形式で保存するカスタムノードです。

### 使い方

1. ComfyUI の音声生成ノードなどの出力を `audio` に接続する。
2. `filename_prefix` に保存ファイル名の接頭辞を設定する。
3. `save_wav` / `save_mp3` / `save_ogg` から保存したい形式を有効にする。
4. ワークフローを実行する。
5. ComfyUI の output ディレクトリに音声ファイルが保存される。

### 入力

- `audio`: ComfyUI の `AUDIO` 入力。
- `filename_prefix`: 保存ファイル名の接頭辞。`audio/se/audio_output` のように書くと、output 配下にサブフォルダを作って保存します。初期値は `audio_output`。
- `save_wav`: WAV 形式で保存する。
- `save_mp3`: MP3 形式で保存する。
- `save_ogg`: OGG 形式で保存する。
- `sample_rate`: 入力音声に sample rate が含まれない場合に使う値。
- `normalize`: 有効にすると、音割れを避けるために音声を正規化する。
- `overwrite`: 有効にすると、連番を付けずに同名ファイルを上書きする。

### 注意点

- MP3 / OGG 保存には `pydub` と ffmpeg が必要です。
- WAV 保存は Python 標準ライブラリで行うため、追加の音声保存ライブラリは不要です。
- batch 音声入力の場合、各batchを別ファイルとして連番保存します。
- 入力音声に `sample_rate` が含まれる場合は、ノード側の `sample_rate` より入力値を優先します。
