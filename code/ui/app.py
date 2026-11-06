"""Ventana principal: ensambla los mixins de ui/ y el core. Aquí solo hay orden de construcción."""
import customtkinter as ctk
from PIL import Image, ImageTk

from core import FasorCalculatorCore
from paths import EXPORT_FILE, SAVED_FILE, resource_path

from .calc_panel import CalcMixin
from .header import HeaderMixin
from .history_panel import HistoryMixin
from .i18n import I18nMixin
from .matrix_panel import MatrixMixin
from .menu_bar import MenuMixin
from .meta import APP_VERSION
from .theming import ThemeMixin


class FasorCalculator(I18nMixin, ThemeMixin, MenuMixin, HeaderMixin, MatrixMixin, HistoryMixin, CalcMixin, ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang = "en"  # antes de cualquier self.t() (incluido el menú)
        self.title(f"Complex Calc v{APP_VERSION}")
        self.geometry("1400x850")
        try:  # HK.jpg es JPEG: requiere PIL -> PhotoImage
            self._icon_image = ImageTk.PhotoImage(Image.open(resource_path("HK.jpg")))
            self.iconphoto(True, self._icon_image)
        except Exception:
            pass

        self.build_menu_bar()
        self.size = 3
        self.saved_items = []
        self.saved_filename = str(SAVED_FILE)
        self.core = FasorCalculatorCore(saved_filename=self.saved_filename, exported_py=str(EXPORT_FILE))
        self.setup_colors()
        self.current_colors = self.themes["dark"].copy()

        self.build_topbar()
        self.build_header()
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=10, pady=10)
        left = ctk.CTkFrame(main)
        left.pack(side="left", padx=10, pady=10)
        self.build_matrix_panel(left)
        self.build_saved_buttons(left)
        right = ctk.CTkFrame(main)
        right.pack(side="right", padx=10, pady=10, fill="both", expand=True)
        self.build_history_panel(right)
        self.build_calc_panel(right)

        self.load_saved_systems()
        self.load_default_example()
        self.apply_theme()
