class PromptCombiner:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template" : ("STRING", {
                    "default": "{base}, {outfit}, {pose}, {background}, {extra}",
                    "multiline": False
                }),
            },
            "optional": {
                "enabled_base": ("BOOLEAN", {"default": True}),
                "base": ("STRING", {"default": "", "multiline": True}),
                "enabled_outfit": ("BOOLEAN", {"default": True}),
                "outfit": ("STRING", {"default": "", "multiline": True}),
                "enabled_pose": ("BOOLEAN", {"default": True}),
                "pose": ("STRING", {"default": "", "multiline": True}),
                "enabled_background": ("BOOLEAN", {"default": True}),
                "background": ("STRING", {"default": "", "multiline": True}),
                "enabled_extra": ("BOOLEAN", {"default": True}),
                "extra": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("concatenated",)
    FUNCTION = "concat"
    CATEGORY = "MyCustomNodes"

    def concat(self, template, enabled_base=True, base="", enabled_outfit=True, outfit="", enabled_pose=True, pose="", enabled_background=True, background="", enabled_extra=True, extra=""):
        parts = {
            "base": base if enabled_base else "",
            "outfit": outfit if enabled_outfit else "",
            "pose": pose if enabled_pose else "",
            "background": background if enabled_background else "",
            "extra": extra if enabled_extra else "",
        }

        return (",".join([p.strip() for p in template.format(**parts).split(",") if p.split()]),)