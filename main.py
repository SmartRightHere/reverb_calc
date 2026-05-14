import customtkinter as ctk
import tkinter as tk
from tkinter import font


class ReverbCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Reverb Time Calculator")
        self.root.geometry("650x400")
        self.root.resizable(False, False)

        # Настройка темы CustomTkinter
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Определяем шрифты
        self.setup_fonts()

        self.create_widgets()

    def setup_fonts(self):
        available_fonts = font.families()

        target_variants = [
            "Segoe UI Variable Display",
            "Segoe UI",
            "SF Pro Display",
            "Inter",
            "Arial"
        ]

        selected_family = "sans-serif"
        for variant in target_variants:
            if variant in available_fonts:
                selected_family = variant
                break

        # Настройка шрифтов с приоритетом Segoe UI
        self.title_font = ctk.CTkFont(family=selected_family, size=22, weight="bold")
        self.header_font = ctk.CTkFont(family=selected_family, size=14, weight="bold")
        self.default_font = ctk.CTkFont(family=selected_family, size=13)
        # Для цифр
        self.mono_font = ctk.CTkFont(family="Consolas" if "Consolas" in available_fonts else "Courier New", size=13)

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Заголовок
        title_label = ctk.CTkLabel(main_frame, text="Reverb Time Calculator",
                                   font=self.title_font)
        title_label.pack(pady=(0, 20))

        # Поле ввода BPM
        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.pack(fill=tk.X, pady=(0, 20))

        ctk.CTkLabel(input_frame, text="BPM",
                     font=self.header_font).pack(side=tk.LEFT, padx=(10, 0), pady=10)

        self.bpm_var = ctk.StringVar(value="140")
        self.bpm_entry = ctk.CTkEntry(input_frame, textvariable=self.bpm_var,
                                      width=100, justify="center", font=self.default_font)
        self.bpm_entry.pack(side=tk.LEFT, padx=10, pady=10)

        self.bpm_var.trace('w', self.on_bpm_changed)

        # Таблица результатов
        self.create_results_table(main_frame)

        # Первоначальный расчет
        self.calculate_reverb()

    def create_results_table(self, parent):
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill=tk.BOTH, expand=True)

        headers = ["Type", "Pre-delay (ms)", "Decay (ms)", "Decay (sec)"]

        for i, header in enumerate(headers):
            label = ctk.CTkLabel(table_frame, text=header,
                                 font=self.header_font)
            label.grid(row=0, column=i, padx=10, pady=10, sticky="ew")

        table_frame.columnconfigure(0, weight=2)
        table_frame.columnconfigure(1, weight=1)
        table_frame.columnconfigure(2, weight=1)
        table_frame.columnconfigure(3, weight=1)

        self.reverb_types = [
            "Hall (2 Bars)",
            "Large Room (1 Bar)",
            "Small Room (1/2 Note)",
            "Tight Ambience (1/4 Note)"
        ]

        self.result_entries = []

        for row, reverb_type in enumerate(self.reverb_types, 1):
            type_label = ctk.CTkLabel(table_frame, text=reverb_type,
                                      font=self.default_font,
                                      width=180, anchor="w")
            type_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

            # Поля результатов
            pre_delay_var = ctk.StringVar()
            pre_delay_entry = ctk.CTkEntry(table_frame, textvariable=pre_delay_var,
                                           state="readonly", width=110, justify="center",
                                           font=self.mono_font)
            pre_delay_entry.grid(row=row, column=1, padx=10, pady=5)

            decay_ms_var = ctk.StringVar()
            decay_ms_entry = ctk.CTkEntry(table_frame, textvariable=decay_ms_var,
                                          state="readonly", width=110, justify="center",
                                          font=self.mono_font)
            decay_ms_entry.grid(row=row, column=2, padx=10, pady=5)

            decay_sec_var = ctk.StringVar()
            decay_sec_entry = ctk.CTkEntry(table_frame, textvariable=decay_sec_var,
                                           state="readonly", width=110, justify="center",
                                           font=self.mono_font)
            decay_sec_entry.grid(row=row, column=3, padx=10, pady=5)

            self.result_entries.append((pre_delay_var, decay_ms_var, decay_sec_var))

    def on_bpm_changed(self, *args):
        self.calculate_reverb()

    def calculate_reverb(self):
        try:
            bpm_text = self.bpm_var.get().strip()
            if not bpm_text:
                self.clear_results()
                return

            bpm = float(bpm_text)
            if bpm <= 0 or bpm > 500:
                self.clear_results()
                return

            beat_time = 60 / bpm
            pre_delay_multipliers = [1 / 8, 1 / 16, 1 / 32, 1 / 64]
            decay_multipliers = [8, 4, 2, 1]

            for i, (pre_delay_mult, decay_mult) in enumerate(zip(pre_delay_multipliers, decay_multipliers)):
                pre_delay = (beat_time * pre_delay_mult) * 1000
                decay_sec = beat_time * decay_mult
                decay_ms = decay_sec * 1000

                pre_delay_var, decay_ms_var, decay_sec_var = self.result_entries[i]

                pre_delay_var.set(f"{pre_delay:.2f}")
                decay_ms_var.set(f"{decay_ms:.2f}")
                decay_sec_var.set(f"{decay_sec:.2f}")

        except ValueError:
            self.clear_results()

    def clear_results(self):
        for pre_delay_var, decay_ms_var, decay_sec_var in self.result_entries:
            pre_delay_var.set("")
            decay_ms_var.set("")
            decay_sec_var.set("")


def main():
    root = ctk.CTk()
    app = ReverbCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# pyinstaller --noconfirm --onefile --windowed --add-data "venv/Lib/site-packages/customtkinter;customtkinter/" --name "ReverbCalcBySmart" --icon="icon.ico" main.py