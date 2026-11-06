"""Textos traducibles (resources/languages.json: 'en' / 'es'). self.t(key, **kw) los resuelve."""
import json

from paths import resource_path


def load_app_text():
    with open(resource_path("languages.json"), "r", encoding="utf-8") as f:
        return json.load(f)


APP_TEXT = load_app_text()

# (atributo del widget, clave en languages.json) que se re-textean al cambiar de idioma
_RETEXT = [
    ("theme_label", "theme_label"), ("lang_label", "lang_label"),
    ("instructions_label", "instructions"), ("btn_change_size", "btn_change_size"),
    ("btn_load_example", "btn_load_example"), ("btn_solve", "btn_solve"),
    ("btn_load_saved", "btn_load_saved"), ("btn_import", "btn_import"),
    ("btn_refresh_saved", "btn_refresh_saved"), ("solution_history_label", "solution_history"),
    ("saved_systems_label", "saved_systems"), ("calc_guide_label", "calc_guide"),
    ("calc_copy_button", "calc_copy_btn"),
]


class I18nMixin:
    lang = "en"

    def t(self, key, **kwargs):
        text = APP_TEXT[self.lang][key]
        return text.format(**kwargs) if kwargs else text

    def change_language(self, display_name):
        """Cambia TODO el texto de la app. Nombres propios/símbolos ('Complex Calc', 'L') no cambian."""
        self.lang = "es" if display_name == "Español" else "en"
        for attr, key in _RETEXT:
            if hasattr(self, attr):
                getattr(self, attr).configure(text=self.t(key))
        self.build_menu_bar()  # el menú es tk puro: más simple reconstruirlo
