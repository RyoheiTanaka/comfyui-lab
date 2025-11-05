import torch

class ImageFilterPreset:
    presets = {
        "none": {
            "brightness": 1.0,
            "contrast": 1.0,
            "gamma": 1.0,
            "saturation": 1.0,
        },
        "vivid": {
            "brightness": 1.15,
            "contrast": 1.3,
            "gamma": 1.5,
            "saturation": 1.5,
        },
        "cinematic": {
            "brightness": 0.85,
            "contrast": 1.4,
            "gamma": 0.9,
            "saturation": 0.7,
        },
        "vintage": {
            "brightness": 1.2,
            "contrast": 0.7,
            "gamma": 1.6,
            "saturation": 0.6,
        },
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "preset": (list(cls.presets.keys()), {"default": "none"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("filtered_image",)
    FUNCTION = "apply_filter"
    CATEGORY = "MyCustomNodes"

    def apply_filter(self, image, preset):
        params = self.presets[preset]
        # 既存のメソッドを順番に適用
        result = self.adjust_brightness(image, params["brightness"])
        result = self.adjust_contrast(result, params["contrast"])
        result = self.adjust_gamma(result, params["gamma"])
        result = self.adjust_saturation(result, params["saturation"])

        return (result,)

    def adjust_brightness(self, image, brightness):
        adjusted = image * brightness
        adjusted = torch.clamp(adjusted, 0.0, 1.0)
        return (adjusted)

    def adjust_contrast(self, image, contrast):
        adjusted = (image - 0.5) * contrast + 0.5
        adjusted = torch.clamp(adjusted, 0.0, 1.0)
        return (adjusted)

    def adjust_gamma(self, image, gamma):
        adjusted = image ** gamma
        adjusted = torch.clamp(adjusted, 0.0, 1.0)
        return (adjusted)
    
    def adjust_saturation(self, image, saturation):
        r = image[..., 0:1]
        g = image[..., 1:2]
        b = image[..., 2:3]
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        adjusted = gray + (image - gray) * saturation
        adjusted = torch.clamp(adjusted, 0.0, 1.0)
        return (adjusted)