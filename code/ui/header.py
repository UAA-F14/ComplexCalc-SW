"""Barra superior (selector de tema/idioma) y encabezado con título, nombres y logo."""
import customtkinter as ctk

from .meta import APP_VERSION, HEADER_NAMES
from .theming import THEME_NAMES
from .widgets import logo_image


class HeaderMixin:
    def build_topbar(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(pady=(10, 6))
        self.theme_label = ctk.CTkLabel(bar, text=self.t("theme_label"), font=("Helvetica", 11))
        self.theme_label.pack(side="left", padx=(0, 5))
        self.theme_selector = ctk.CTkOptionMenu(bar, values=THEME_NAMES, command=self.change_theme, width=120)
        self.theme_selector.set("Dark")
        self.theme_selector.pack(side="left")

        self.lang_label = ctk.CTkLabel(bar, text=self.t("lang_label"), font=("Helvetica", 11))
        self.lang_label.pack(side="left", padx=(15, 5))
        self.lang_selector = ctk.CTkOptionMenu(bar, values=["English", "Español"], command=self.change_language, width=100)
        self.lang_selector.set("English")
        self.lang_selector.pack(side="left")

    def build_header(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 10), padx=12)
        self.header_title = ctk.CTkLabel(frame, text=f"Complex Calc {APP_VERSION}", font=("Helvetica", 28, "bold"))
        self.header_title.pack(side="left", padx=(0, 12))
        self.header_names = ctk.CTkLabel(frame, text=HEADER_NAMES, font=("Helvetica", 17))
        self.header_names.pack(side="left", padx=(0, 8), pady=(8, 0))
        logo = logo_image(75)
        if logo:
            self.ie_label = ctk.CTkLabel(frame, image=logo, text="", fg_color="transparent")
            self.ie_label.image = logo
            self.ie_label.pack(side="left", padx=(6, 0))
