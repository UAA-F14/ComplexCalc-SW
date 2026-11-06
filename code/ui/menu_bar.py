"""Barra de menú (File / Help) y diálogo About."""
import tkinter as tk
import webbrowser

import customtkinter as ctk

from .meta import APP_VERSION, CREATORS, DEPARTMENT, GITHUB_URL, INSTITUTION, LAST_UPDATED
from .widgets import center_over, logo_image

LINK = "#3498DB"


class MenuMixin:
    def build_menu_bar(self):
        """Menú nativo. Reutiliza los mismos comandos de los botones; no duplica lógica."""
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        for key, cmd in (("menu_save_current", self.solve), ("menu_import", self.import_from_file),
                         ("menu_load_saved", self.load_saved_menu_popup),
                         ("menu_refresh_saved", self.load_saved_systems)):
            file_menu.add_command(label=self.t(key), command=cmd)
        file_menu.add_separator()
        file_menu.add_command(label=self.t("menu_exit"), command=self.destroy)
        menubar.add_cascade(label=self.t("menu_file"), menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label=self.t("menu_about"), command=self.show_about_dialog)
        menubar.add_cascade(label=self.t("menu_help"), menu=help_menu)
        self.configure(menu=menubar)

    def show_about_dialog(self):
        """Modal temático: versión, fecha, repo, creadores e institución."""
        c = self.current_colors
        frame_color, label_color = c.get("frame", "#2d2d2d"), c.get("label_text", "#FFFFFF")

        dlg = ctk.CTkToplevel(self)
        dlg.title(self.t("about_title"))
        dlg.transient(self)
        dlg.configure(fg_color=frame_color)
        dlg.resizable(False, False)
        content = ctk.CTkFrame(dlg, fg_color=frame_color)
        content.pack(padx=20, pady=16)

        def label(text, size, bold="", color=label_color, link=False, **pack):
            lb = ctk.CTkLabel(content, text=text, font=("Helvetica", size, *([bold] if bold else [])),
                              text_color=color, **({"cursor": "hand2"} if link else {}))
            lb.pack(**pack)
            return lb

        logo = logo_image(80)
        if logo:
            lb = ctk.CTkLabel(content, image=logo, text="", fg_color="transparent")
            lb.image = logo
            lb.pack(pady=(0, 8))

        label(self.t("about_heading"), 20, "bold")
        label(self.t("about_version", version=APP_VERSION, date=LAST_UPDATED), 12, pady=(2, 10))
        label(f"{INSTITUTION}\n{DEPARTMENT}", 12, pady=(0, 10))
        gh = label(self.t("about_github"), 12, "underline", LINK, link=True, pady=(0, 12))
        gh.bind("<Button-1>", lambda _e: webbrowser.open(GITHUB_URL))
        label(self.t("about_creators"), 13, "bold", pady=(0, 4))

        for cr in CREATORS:
            if cr["email"]:
                label(cr["name"], 12)
                em = label(cr["email"], 11, "underline", LINK, link=True, pady=(0, 6))
                em.bind("<Button-1>", lambda _e, a=cr["email"]: webbrowser.open(f"mailto:{a}"))
            else:
                label(cr["name"], 12, pady=(0, 6))

        ctk.CTkButton(content, text=self.t("about_close"), width=100, command=dlg.destroy,
                      fg_color=c.get("button", "#3a3a3a"), hover_color=c.get("button_hover", "#4a4a4a"),
                      text_color=c.get("button_text", "#FFFFFF")).pack(pady=(10, 0))
        dlg.bind("<Escape>", lambda _e: dlg.destroy())
        center_over(dlg, self)
        dlg.update()
        dlg.grab_set()
