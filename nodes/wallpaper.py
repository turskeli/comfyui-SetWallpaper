import os
import ctypes
import winreg
from sys import platform
import numpy as np
from PIL import Image

class SetWallpaper:
    def __init__(self):
        self.styles = {
            "center": 0, 
            "fill": 10,
            "fit": 6,
            "span": 22,
            "stretch": 2,
            "tile": 0,
        }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "style": (["center","fill","fit","span","stretch","tile"],),
            },
        }

    RETURN_TYPES = ()

    FUNCTION = "doIt"

    OUTPUT_NODE = True

    CATEGORY = "Wallpaper"

    def doIt(self, image, style, tile):
        out = os.path.join(os.path.abspath(os.path.dirname(__file__)), "background.png")
        if not platform.startswith("win"):
            raise Exception("Currently, wallpaper is only supported on Windows platforms")
        if style not in self.styles:
            raise Exception(f"Style of '{style}' is not supported")
        print(f"Saving to {out} and setting background")
        i = 255. * image[0].cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        img.save(out)
        self.set_wallpaper_style(self.styles[style],tile)
        self.set_wallpaper(out)

        return {}

    def set_wallpaper(self, path):
        SPI_SETDESKTOPWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKTOPWALLPAPER, 0, path, 3)

    def set_wallpaper_style(self, style, tile):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               "Control Panel\\Desktop", 0, winreg.KEY_ALL_ACCESS)
        if style == "tile":
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "1")
        else:
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, str(style))
        winreg.CloseKey(key)
