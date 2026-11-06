"""Panel izquierdo: instrucciones, matriz A y vector b, tamaño, ejemplo y botón Solve."""
from tkinter import messagebox

import customtkinter as ctk

from .widgets import center_over

EXAMPLE_A = [["2+1i", "-1", "0"], ["-1", "2+0.5i", "-1"], ["0", "-1", "2"]]
EXAMPLE_B = ["1", "0", "1i"]


class MatrixMixin:
    def build_matrix_panel(self, left):
        info_frame = ctk.CTkFrame(left)
        info_frame.pack(pady=10)
        text_frame = ctk.CTkFrame(info_frame)
        text_frame.pack(side="left", padx=10)
        self.instructions_label = ctk.CTkLabel(text_frame, text=self.t("instructions"), justify="left", anchor="w")
        self.instructions_label.pack(pady=5)

        self.btn_change_size = ctk.CTkButton(left, text=self.t("btn_change_size"), command=self.change_size)
        self.btn_change_size.pack(pady=5)
        self.btn_load_example = ctk.CTkButton(left, text=self.t("btn_load_example"), command=self.load_default_example)
        self.btn_load_example.pack(pady=5)

        self.frame_matrix = ctk.CTkFrame(left)
        self.frame_matrix.pack(pady=10)
        self.build_matrix()
        self.btn_solve = ctk.CTkButton(left, text=self.t("btn_solve"), command=self.solve)
        self.btn_solve.pack(pady=10)

    # ---------- matriz ----------
    def _new_entry(self, row, col, text):
        c = self.current_colors
        e = ctk.CTkEntry(self.frame_matrix, width=130, fg_color=c.get("entry", "#333333"),
                         text_color=c.get("entry_text", "#FFFFFF"), border_color=c.get("border", "#555555"))
        e.grid(row=row, column=col, padx=3, pady=3)
        e.insert(0, text)
        return e

    def build_matrix(self):
        for w in self.frame_matrix.winfo_children():
            w.destroy()
        n = self.size
        self.entries_A = [[self._new_entry(i, j, "1L0") for j in range(n)] for i in range(n)]
        ctk.CTkLabel(self.frame_matrix, text="  |  ",
                     text_color=self.current_colors.get("label_text", "#FFFFFF"),
                     fg_color="transparent").grid(row=0, column=n, rowspan=n)
        self.entries_b = [self._new_entry(i, n + 1, "0") for i in range(n)]
        self.apply_theme()

    def fill_entries(self, A_vals, b_vals):
        """Rellena A y b (tolera desajustes de tamaño dejando el valor por defecto)."""
        def put(entry, value):
            entry.delete(0, "end")
            entry.insert(0, value)
        for i in range(min(self.size, len(A_vals))):
            for j in range(min(self.size, len(A_vals[i]))):
                put(self.entries_A[i][j], A_vals[i][j])
        for i in range(min(self.size, len(b_vals))):
            put(self.entries_b[i], b_vals[i])

    def load_default_example(self):
        """Ejemplo 3x3 en rectangular con 'i' como unidad imaginaria."""
        if self.size != 3:
            self.size = 3
            self.build_matrix()
        self.fill_entries(EXAMPLE_A, EXAMPLE_B)

    # ---------- resolver ----------
    def solve(self):
        try:
            A = [[e.get() for e in row] for row in self.entries_A]
            b = [e.get() for e in self.entries_b]
            result = self.core.solve_from_strings(A, b)
            self.add_to_history_view(result)
            try:
                self.core.save_system(result)
            except Exception as e:
                messagebox.showwarning(self.t("warning_title"), self.t("msg_could_not_save", err=e))
        except Exception as e:
            messagebox.showerror(self.t("error_title"), self.t("msg_invalid_or_singular", err=e))

    # ---------- tamaño ----------
    def change_size(self):
        result = self._themed_size_dialog(current=self.size)
        if result is None:
            return
        try:
            new_size = int(result)
            if 1 <= new_size <= 10:
                self.size = new_size
                self.build_matrix()
            else:
                messagebox.showwarning(self.t("warning_title"), self.t("msg_size_range"))
        except ValueError:
            messagebox.showerror(self.t("error_title"), self.t("msg_invalid_number"))

    def _themed_size_dialog(self, current=None):
        """Modal temático para pedir el tamaño. Devuelve el texto ingresado o None si se cancela."""
        c = self.current_colors
        frame_color = c.get("frame", "#2d2d2d")
        btn = dict(width=80, fg_color=c.get("button", "#FF69B4"), hover_color=c.get("button_hover", "#FF1493"),
                   text_color="#FFFFFF")

        dlg = ctk.CTkToplevel(self)
        dlg.title(self.t("size_dialog_title"))
        dlg.transient(self)
        dlg.configure(fg_color=frame_color)
        ctk.CTkLabel(dlg, text=self.t("size_dialog_label"), text_color=c.get("label_text", "#FFFFFF")).pack(padx=12, pady=(12, 6))
        entry = ctk.CTkEntry(dlg, width=120, fg_color=c.get("entry", "#333333"),
                             text_color=c.get("entry_text", "#FFFFFF"), border_color=c.get("border", "#555555"))
        entry.pack(padx=12, pady=(0, 12))
        if current is not None:
            entry.insert(0, str(current))
        entry.focus_set()

        res = {"value": None}

        def on_ok():
            res["value"] = entry.get()
            dlg.destroy()

        btn_frame = ctk.CTkFrame(dlg, fg_color=frame_color)
        btn_frame.pack(padx=12, pady=(0, 12))
        ctk.CTkButton(btn_frame, text=self.t("size_ok"), command=on_ok, **btn).grid(row=0, column=0, padx=6)
        ctk.CTkButton(btn_frame, text=self.t("size_cancel"), command=dlg.destroy, **btn).grid(row=0, column=1, padx=6)
        dlg.bind("<Return>", lambda e: on_ok())
        dlg.bind("<Escape>", lambda e: dlg.destroy())

        center_over(dlg, self)
        dlg.update()
        dlg.grab_set()  # después de posicionar y mostrar
        dlg.wait_window()
        return res["value"]
