"""
ComfyUI Lab - Custom Nodes Collection
Learning project for ComfyUI custom node development
"""

from .nodes import prompt_combiner, brightness_adjust, contrast_adjust, gamma_adjust, saturation_adjust
from .nodes import image_filter_preset, color_temperature_adjust


NODE_CLASS_MAPPINGS = {
    "PromptCombiner": prompt_combiner.PromptCombiner,
    "BrightnessAdjust": brightness_adjust.BrightnessAdjust,
    "ContrastAdjust": contrast_adjust.ContrastAdjust,
    "GammaAdjust": gamma_adjust.GammaAdjust,
    "SaturationAdjust": saturation_adjust.SaturationAdjust,
    "ImageFilterPreset": image_filter_preset.ImageFilterPreset,
    "ColorTemperatureAdjust": color_temperature_adjust.ColorTemperatureAdjust,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptCombiner": "Prompt Combiner",
    "BrightnessAdjust": "Brightness Adjust",
    "ContrastAdjust": "Contrast Adjust",
    "GammaAdjust": "Gamma Adjust",
    "SaturationAdjust": "Saturation Adjust",
    "ImageFilterPreset": "Image Filter Preset",
    "ColorTemperatureAdjust": "Color Temperature Adjust",
}