import torch

class ContrastAdjust:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "contrast": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 3.0,
                    "step": 0.01
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("adjusted_image",)
    FUNCTION = "adjust_contrast"
    CATEGORY = "MyCustomNodes"

    def adjust_contrast(self, image, contrast):
        # コントラストを調整する
        # 1. 中心(0.5)を基準にする
        # 2. contrast倍する
        # 3. 中心を元に戻す
        adjusted = (image - 0.5) * contrast + 0.5

        # 0.0から1.0の範囲にクリップする
        adjusted = torch.clamp(adjusted, 0.0, 1.0)

        return (adjusted,)