import torch

class ImageFilterPreset:
    presets = {
        "none": {
            "brightness": 1.0,
            "contrast": 1.0,
            "gamma": 1.0,
            "saturation": 1.0,
            "temperature": 1.0,
        },
        "vivid": {
            "brightness": 1.08,
            "contrast": 1.2,
            "gamma": 1.3,
            "saturation": 1.3,
            "temperature": 1.15,
        },
        "cinematic": {
            "brightness": 0.9,
            "contrast": 1.5,
            "gamma": 0.85,
            "saturation": 0.65,
            "temperature": 0.85,
        },
        "vintage": {
            "brightness": 1.2,
            "contrast": 0.7,
            "gamma": 1.6,
            "saturation": 0.6,
            "temperature": 1.3,
        },
        "warm_sunset": {
            "brightness": 1.1,
            "contrast": 1.1,
            "gamma": 1.3,
            "saturation": 1.2,
            "temperature": 1.5,
        },
        "cool_morning": {
            "brightness": 1.0,
            "contrast": 1.15,
            "gamma": 1.1,
            "saturation": 1.1,
            "temperature": 0.6,
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
        result = self.adjust_temperature(result, params["temperature"])

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

    def adjust_temperature(self, image, temperature):
        adjusted = image.clone()
        adjusted[:, :, :, 0] = adjusted[:, :, :, 0] * temperature      # R
        adjusted[:, :, :, 2] = adjusted[:, :, :, 2] / temperature      # B
        adjusted = torch.clamp(adjusted, 0.0, 1.0)
        return (adjusted)