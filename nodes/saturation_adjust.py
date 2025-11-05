import torch
import torch.nn.functional as F

class SaturationAdjust:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "saturation": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("adjusted_image",)
    FUNCTION = "adjust_saturation"
    CATEGORY = "MyCustomNodes"

    def adjust_saturation(self, image, saturation):
        # グレースケール（明度）を計算
        # 人間の目の感度に合わせた重み付け
        r = image[..., 0:1]
        g = image[..., 1:2]
        b = image[..., 2:3]
        
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        
        # 元の画像とグレースケールを補間
        # saturation = 0.0 → グレースケール
        # saturation = 1.0 → 元の色
        # saturation > 1.0 → より鮮やか
        adjusted = gray + (image - gray) * saturation
        
        # 範囲制限
        adjusted = torch.clamp(adjusted, 0.0, 1.0)
        
        return (adjusted,)