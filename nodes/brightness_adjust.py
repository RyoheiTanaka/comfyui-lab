import torch

class BrightnessAdjust:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "brightness": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("adjusted_image",)
    FUNCTION = "adjust_brightness"
    CATEGORY = "MyCustomNodes"

    def adjust_brightness(self, image, brightness=1.0):
        adjusted = image * brightness
        adjusted = torch.clamp(adjusted, 0.0, 1.0)
        return (adjusted,)