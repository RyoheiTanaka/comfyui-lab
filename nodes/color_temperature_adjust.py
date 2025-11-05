import torch

class ColorTemperatureAdjust:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "temperature": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.01
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("adjusted_image",)
    FUNCTION = "adjust_temperature"
    CATEGORY = "MyCustomNodes"

    def adjust_temperature(self, image, temperature):
        # 色温度調整
        # temperature > 1.0: 暖色（オレンジ/黄色っぽく）
        # temperature < 1.0: 寒色（青っぽく）
        adjusted = image.clone()

        # temperature = 1.0 のときは何もしない
        # temperature > 1.0: 赤強く、青弱く（暖色）
        # temperature < 1.0: 赤弱く、青強く（寒色）
        adjusted[:, :, :, 0] = adjusted[:, :, :, 0] * temperature      # R
        adjusted[:, :, :, 2] = adjusted[:, :, :, 2] / temperature      # B

        adjusted = torch.clamp(adjusted, 0.0, 1.0)

        return (adjusted,)