from .nodes import PromptCombiner, BrightnessAdjust

NODE_CLASS_MAPPINGS = {
    "PromptCombiner": PromptCombiner,
    "BrightnessAdjust": BrightnessAdjust
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptCombiner": "Prompt Combiner",
    "BrightnessAdjust": "Brightness Adjust"
}