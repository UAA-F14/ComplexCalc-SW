"""Helpers de widgets compartidos por varios módulos de UI."""
import customtkinter as ctk
from PIL import Image

from paths import resource_path


def logo_image(size):
    """Logo IE como CTkImage (size x size) o None si falta el archivo."""
    try:
        img = Image.open(resource_path("IE.png"))
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))
    except Exception:
        return None


def center_over(dlg, parent):
    """Centra el diálogo sobre su ventana padre."""
    dlg.update_idletasks()
    w, h = dlg.winfo_reqwidth(), dlg.winfo_reqheight()
    x = parent.winfo_rootx() + parent.winfo_width() // 2 - w // 2
    y = parent.winfo_rooty() + parent.winfo_height() // 2 - h // 2
    dlg.geometry(f"+{x}+{y}")
