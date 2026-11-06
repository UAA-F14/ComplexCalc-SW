"""Calculadora auxiliar (AUX Calc): teclado, display y conversión fasor <-> rectangular."""
from tkinter import messagebox

import customtkinter as ctk

from core import complejo_a_fasor, format_rect_result

# 'L' escribe notación fasorial (entrada real). '⇄' y '📋' son ACCIONES y van aparte del teclado.
KEYPAD = [
    ["7", "8", "9", "/", "C", "⌫"],
    ["4", "5", "6", "*", "(", "L"],
    ["1", "2", "3", "-", ")"],
    ["0", ".", "j", "+", "="],
]
OPERATORS = ("+", "-", "*", "/", "^")
INPUT_KEYS = tuple("0123456789.j()L")


class CalcMixin:
    def build_calc_panel(self, right):
        frame = ctk.CTkFrame(right, border_width=1, border_color="#444444", width=300, height=360)
        frame.pack(pady=5, padx=10)
        frame.pack_propagate(False)
        ctk.CTkLabel(frame, text="AUX Calc", font=("Helvetica", 12, "bold")).pack(pady=2)

        self.calc_display = ctk.CTkEntry(frame, width=260, height=40, font=("Courier New", 14, "bold"), justify="right")
        self.calc_display.pack(pady=3, padx=8)
        self.calc_display.insert(0, "0")
        self.calc_display.bind("<Return>", lambda _e: self.calc_button_click("="))

        pad = ctk.CTkFrame(frame)
        pad.pack(pady=3, padx=8)
        self.calc_buttons = []
        for i, row in enumerate(KEYPAD):
            for j, key in enumerate(row):
                btn = ctk.CTkButton(pad, text=key, width=42, height=32, font=("Helvetica", 11, "bold"),
                                    command=lambda k=key: self.calc_button_click(k))
                btn.grid(row=i, column=j, padx=1, pady=1)
                self.calc_buttons.append(btn)

        self.calc_guide_label = ctk.CTkLabel(frame, text=self.t("calc_guide"), font=("Helvetica", 9),
                                             text_color="#999999", justify="left")
        self.calc_guide_label.pack(pady=(6, 2), padx=8, anchor="w")

        # acciones sobre el resultado, separadas del teclado de entrada
        self.calc_copy_button = ctk.CTkButton(frame, text=self.t("calc_copy_btn"), height=28, width=90,
                                              font=("Helvetica", 10, "bold"),
                                              command=lambda: self.calc_button_click("📋"))
        self.calc_copy_button.pack(pady=(0, 4), padx=8, anchor="e")
        toggle_btn = ctk.CTkButton(frame, text="r∠θ  ⇄  a+jb", height=32, font=("Helvetica", 12, "bold"),
                                   command=lambda: self.calc_button_click("⇄"))
        toggle_btn.pack(pady=(0, 2), padx=8, fill="x")
        self.calc_action_buttons = [self.calc_copy_button, toggle_btn]
        ctk.CTkLabel(frame, text="").pack(pady=2)

    def _calc_show(self, text):
        self.calc_display.delete(0, "end")
        self.calc_display.insert(0, text)

    def calc_button_click(self, key):
        cur = self.calc_display.get()
        try:
            if key == "C":
                self._calc_show("0")
            elif key == "⌫":
                self._calc_show(cur[:-1] or "0")
            elif key in ("=", "⇄"):
                try:
                    z = self.core.evaluate_expression(cur)
                    # '⇄' invierte la forma actual: si ya es fasor ('L' o '∠') -> rectangular, si no -> fasor
                    to_rect = key == "=" or "L" in cur.upper() or "∠" in cur
                    self._calc_show(format_rect_result(z) if to_rect else complejo_a_fasor(z))
                except Exception as e:
                    messagebox.showerror(self.t("error_title"), self.t("calc_invalid_expr", expr=cur, err=e))
            elif key == "📋":
                self.clipboard_clear()
                self.clipboard_append(cur)  # pegable con Ctrl+V en cualquier celda de A/b
            elif key in OPERATORS:
                if cur and cur != "0":
                    self.calc_display.insert("end", "**" if key == "^" else key)
            elif key in INPUT_KEYS:
                if cur == "0" and key != ".":
                    self._calc_show(key)
                else:
                    self.calc_display.insert("end", key)
        except Exception as e:
            messagebox.showerror(self.t("error_title"), self.t("calc_error", err=e))
