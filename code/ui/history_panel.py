"""Panel derecho (historial de soluciones) y sistemas guardados: lista, carga e importación."""
from tkinter import filedialog, messagebox

import customtkinter as ctk


class HistoryMixin:
    def build_history_panel(self, right):
        self.solution_history_label = ctk.CTkLabel(right, text=self.t("solution_history"))
        self.solution_history_label.pack()
        self.history_box = ctk.CTkTextbox(right, width=720, height=280)
        self.history_box.pack(pady=5)

        self.saved_systems_label = ctk.CTkLabel(right, text=self.t("saved_systems"))
        self.saved_systems_label.pack()
        self.saved_menu = ctk.CTkOptionMenu(right, values=["(empty)"], command=self.load_saved_option)
        self.saved_menu.pack(pady=5)

    def build_saved_buttons(self, left):
        frame = ctk.CTkFrame(left)
        frame.pack(pady=5)
        for col, (attr, key, cmd) in enumerate((
                ("btn_load_saved", "btn_load_saved", self.load_saved_menu_popup),
                ("btn_import", "btn_import", self.import_from_file),
                ("btn_refresh_saved", "btn_refresh_saved", self.load_saved_systems))):
            btn = ctk.CTkButton(frame, text=self.t(key), command=cmd)
            btn.grid(row=0, column=col, padx=5)
            setattr(self, attr, btn)

    def add_to_history_view(self, result):
        box, x_p, x_r = self.history_box, result["x_polar"], result["x_rect"]
        box.insert("end", f"\n=== SOLUTION ===\nSaved: {result['timestamp']}\n\n\nSolution:\n")
        for i in range(result["size"]):
            box.insert("end", f"  x{i+1} = {x_p[i]}   |   {x_r[i]}\n")
        box.insert("end", "\n----------------------------\n")

    # ---------- lista de guardados ----------
    def _show_saved_items(self):
        labels = [f"{self.t('saved_item_label')} #{i} — {obj.get('timestamp', 'unknown time')}"
                  for i, obj in enumerate(self.saved_items, start=1)]
        self.saved_menu.configure(values=labels)
        self.saved_menu.set(labels[-1])

    def load_saved_systems(self):
        """Lee saved_systems.txt y rellena self.saved_items y el desplegable."""
        empty = self.t("empty_saved_list")
        try:
            self.saved_items = self.core.load_saved_items()
            if not self.saved_items:
                self.saved_menu.configure(values=["(vacio)"])
                self.saved_menu.set(empty)
                return
            self._show_saved_items()
        except Exception as e:
            messagebox.showwarning(self.t("warning_title"),
                                   self.t("msg_could_not_read", file=self.saved_filename, err=e))
            self.saved_menu.configure(values=[empty])
            self.saved_menu.set(empty)

    def load_saved_option(self, option_text):
        """Callback del desplegable: carga el sistema elegido en la matriz."""
        if not option_text or option_text in ("(vacio)", self.t("empty_saved_list")):
            return
        try:
            self._load_saved_by_index(int(option_text.split("#")[1].split(" ")[0]) - 1)
        except Exception as e:
            messagebox.showerror(self.t("error_title"), self.t("msg_could_not_load_selected", err=e))

    def _load_saved_by_index(self, idx):
        err = lambda key: messagebox.showerror(self.t("error_title"), self.t(key))
        if idx < 0 or idx >= len(self.saved_items):
            return err("msg_invalid_saved_index")
        obj = self.saved_items[idx]
        if not obj.get("size"):
            return err("msg_missing_size_info")

        self.size = obj["size"]
        self.build_matrix()
        A_p, b_p = obj.get("A_polar"), obj.get("b_polar")
        if A_p is None or b_p is None:
            return err("msg_missing_polar_info")
        self.fill_entries(A_p, b_p)
        messagebox.showinfo(self.t("done_title"), self.t("msg_loaded_done", n=idx + 1))

    def load_saved_menu_popup(self):
        """Refresca la lista de guardados y avisa."""
        self.load_saved_systems()
        messagebox.showinfo(self.t("info_title"), self.t("msg_list_updated"))

    def import_from_file(self):
        """Elige otro archivo de guardados y carga sus entradas en el desplegable."""
        path = filedialog.askopenfilename(title=self.t("select_saved_file_title"),
                                          filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        try:
            imported = self.core.import_from_file(path)
            if not imported:
                messagebox.showwarning(self.t("warning_title"), self.t("msg_no_valid_entries"))
                return
            self.saved_items = imported
            self._show_saved_items()
            messagebox.showinfo(self.t("imported_title"), self.t("msg_imported", n=len(imported), path=path))
        except Exception as e:
            messagebox.showerror(self.t("error_title"), self.t("msg_could_not_import", err=e))
