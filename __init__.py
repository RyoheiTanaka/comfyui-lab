"""
ComfyUI Lab - Custom Nodes Collection
Learning project for ComfyUI custom node development
"""

from .nodes import prompt_combiner
from .nodes import brightness_adjust

NODE_CLASS_MAPPINGS = {
    "PromptCombiner": prompt_combiner.PromptCombiner,
    "BrightnessAdjust": brightness_adjust.BrightnessAdjust
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptCombiner": "Prompt Combiner",
    "BrightnessAdjust": "Brightness Adjust"
}