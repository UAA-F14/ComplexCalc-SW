"""Temas de color (resources/themes.json) y su aplicación a todos los widgets."""
import json

import customtkinter as ctk

from paths import resource_path

THEME_NAMES = ["Dark", "Light", "Pink", "Mint", "Purple", "Ocean"]


class ThemeMixin:
    def setup_colors(self):
        with open(resource_path("themes.json"), "r", encoding="utf-8") as f:
            self.themes = json.load(f)  # claves en minúsculas: dark, light, pink, ...

    def change_theme(self, theme_name):
        ctk.set_appearance_mode("dark")  # la paleta propia manda; CTk siempre en dark
        self.current_colors = self.themes.get(theme_name.lower(), self.themes["dark"]).copy()
        self.apply_theme()

    def apply_theme(self):
        """Pinta la ventana y todos los widgets con self.current_colors."""
        c = self.current_colors
        btn = dict(fg_color=c["button"], text_color=c.get("button_text", "#FFFFFF"), hover_color=c["button_hover"])
        self.configure(fg_color=c["bg"])
        for w in self._get_all_widgets(self):
            if isinstance(w, ctk.CTkFrame):
                w.configure(fg_color=c["frame"])
            elif isinstance(w, ctk.CTkLabel):
                w.configure(fg_color="transparent", text_color=c["label_text"])
            elif isinstance(w, ctk.CTkButton):
                w.configure(**btn)
            elif isinstance(w, ctk.CTkEntry):
                w.configure(fg_color=c["entry"], text_color=c["entry_text"], border_color=c["border"])
            elif isinstance(w, ctk.CTkOptionMenu):
                self._style_option_menu(w)
            elif isinstance(w, ctk.CTkTextbox):
                w.configure(fg_color=c["textbox"], text_color=c["text"])

    def _style_option_menu(self, w):
        c = self.current_colors
        w.configure(fg_color=c["button"], text_color=c["label_text"], button_color=c["button_hover"])
        menu = getattr(w, "_menu", None)  # tk.Menu interno del desplegable
        if menu is None:
            return
        style = dict(background=c["frame"], foreground=c["label_text"], activebackground=c["button"],
                     activeforeground=c.get("button_text", "#FFFFFF"))
        try:
            menu.configure(**style)
            for i in range((menu.index("end") or -1) + 1):
                try:
                    menu.entryconfigure(i, **style)
                except Exception:
                    pass
        except Exception:
            pass

    def _get_all_widgets(self, parent):
        widgets = []
        for w in parent.winfo_children():
            widgets.append(w)
            widgets.extend(self._get_all_widgets(w))
        return widgets
