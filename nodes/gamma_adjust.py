import torch

class GammaAdjust:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "gamma": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.01
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("adjusted_image",)
    FUNCTION = "adjust_gamma"
    CATEGORY = "MyCustomNodes"

    def adjust_gamma(self, image, gamma):
        # ガンマ補正(べき乗するだけ)
        adjusted = image ** gamma

        # 0.0から1.0の範囲にクリップする
        adjusted = torch.clamp(adjusted, 0.0, 1.0)

        return (adjusted,)