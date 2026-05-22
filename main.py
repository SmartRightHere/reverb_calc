import customtkinter as ctk
import tkinter as tk
from tkinter import font

class ReverbCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Reverb Time Calculator")
        self.root.geometry("780x580")
        self.root.resizable(False, False)

        # Студийный темный дизайн с акцентом
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green") 

        self.setup_fonts()
        self.result_entries = {}
        self.create_widgets()

    def setup_fonts(self):
        available_fonts = font.families()

        target_variants = [
            "Segoe UI Variable Display",
            "SF Pro Display",
            "Inter",
            "Segoe UI",
            "Arial"
        ]

        selected_family = "sans-serif"
        for variant in target_variants:
            if variant in available_fonts:
                selected_family = variant
                break

        self.title_font = ctk.CTkFont(family=selected_family, size=28, weight="bold")
        self.header_font = ctk.CTkFont(family=selected_family, size=15, weight="bold")
        self.default_font = ctk.CTkFont(family=selected_family, size=14)
        self.mono_font = ctk.CTkFont(family="Consolas" if "Consolas" in available_fonts else "Courier New", size=14, weight="bold")

    def create_widgets(self):
        # Главный контейнер
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)

        # Заголовок
        title_label = ctk.CTkLabel(main_frame, text="Reverb Time Calculator", font=self.title_font)
        title_label.pack(anchor="w", pady=(0, 20))

        # Карточка управления BPM
        control_card = ctk.CTkFrame(main_frame, corner_radius=12)
        control_card.pack(fill=tk.X, pady=(0, 25), ipadx=15, ipady=15)

        bpm_top_frame = ctk.CTkFrame(control_card, fg_color="transparent")
        bpm_top_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        ctk.CTkLabel(bpm_top_frame, text="TEMPO (BPM)", font=self.header_font, text_color="gray70").pack(side=tk.LEFT)

        self.bpm_var = ctk.StringVar(value="140")
        self.bpm_entry = ctk.CTkEntry(bpm_top_frame, textvariable=self.bpm_var, 
                                      width=90, height=35, justify="center", 
                                      font=self.header_font, corner_radius=8, border_width=1)
        self.bpm_entry.pack(side=tk.RIGHT)
        self.bpm_var.trace('w', self.on_bpm_changed)

        # Слайдер для BPM
        self.bpm_slider = ctk.CTkSlider(control_card, from_=50, to=250, command=self.on_slider_changed)
        self.bpm_slider.set(140)
        self.bpm_slider.pack(fill=tk.X, padx=10, pady=(10, 10))

        # Карточка с результатами (вкладки)
        results_card = ctk.CTkFrame(main_frame, corner_radius=12, fg_color="transparent")
        results_card.pack(fill=tk.BOTH, expand=True)

        self.tabview = ctk.CTkTabview(results_card, corner_radius=10)
        self.tabview.pack(fill=tk.BOTH, expand=True)

        self.modes = ["Straight", "Dotted", "Triplet"]
        
        for mode in self.modes:
            tab = self.tabview.add(mode)
            self.result_entries[mode] = []
            self.create_results_table(tab, mode)

        self.calculate_reverb()

    def create_results_table(self, parent, mode):
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        headers = ["Room Size", "Pre-delay (ms)", "Decay (ms)", "Decay (sec)"]

        # Отрисовка заголовков таблицы
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(table_frame, text=header, font=self.header_font, text_color="gray70")
            label.grid(row=0, column=i, padx=10, pady=(0, 15), sticky="w" if i == 0 else "")

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

        # Отрисовка строк
        for row, reverb_type in enumerate(self.reverb_types, 1):
            # Название размера
            type_label = ctk.CTkLabel(table_frame, text=reverb_type, font=self.default_font)
            type_label.grid(row=row, column=0, padx=10, pady=10, sticky="w")

            # Стиль для полей вывода (имитация цифрового дисплея)
            entry_kwargs = {
                "state": "readonly",
                "width": 110,
                "height": 32,
                "justify": "center",
                "font": self.mono_font,
                "fg_color": "#1e1e1e", # Более темный фон для контраста
                "border_width": 0,
                "corner_radius": 6
            }

            pre_delay_var = ctk.StringVar()
            pre_delay_entry = ctk.CTkEntry(table_frame, textvariable=pre_delay_var, **entry_kwargs)
            pre_delay_entry.grid(row=row, column=1, padx=10, pady=10)

            decay_ms_var = ctk.StringVar()
            decay_ms_entry = ctk.CTkEntry(table_frame, textvariable=decay_ms_var, **entry_kwargs)
            decay_ms_entry.grid(row=row, column=2, padx=10, pady=10)

            decay_sec_var = ctk.StringVar()
            decay_sec_entry = ctk.CTkEntry(table_frame, textvariable=decay_sec_var, **entry_kwargs)
            decay_sec_entry.grid(row=row, column=3, padx=10, pady=10)

            self.result_entries[mode].append((pre_delay_var, decay_ms_var, decay_sec_var))

    def on_slider_changed(self, value):
        # Обновляем поле ввода при движении слайдера
        self.bpm_var.set(str(int(value)))

    def on_bpm_changed(self, *args):
        try:
            # Пытаемся обновить ползунок, если значение ввели руками
            val = float(self.bpm_var.get())
            if 30 <= val <= 300:
                self.bpm_slider.set(val)
        except ValueError:
            pass
        
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

            modifiers = {
                "Straight": 1.0,
                "Dotted": 1.5,
                "Triplet": 2.0 / 3.0
            }

            for mode in self.modes:
                mod = modifiers[mode]
                
                for i, (pre_delay_mult, decay_mult) in enumerate(zip(pre_delay_multipliers, decay_multipliers)):
                    pre_delay = (beat_time * pre_delay_mult * mod) * 1000
                    decay_total_ms = (beat_time * decay_mult * mod) * 1000
                    
                    decay_ms_true = max(0, decay_total_ms - pre_delay)
                    decay_sec_true = decay_ms_true / 1000

                    pre_delay_var, decay_ms_var, decay_sec_var = self.result_entries[mode][i]

                    pre_delay_var.set(f"{pre_delay:.2f}")
                    decay_ms_var.set(f"{decay_ms_true:.2f}")
                    decay_sec_var.set(f"{decay_sec_true:.2f}")

        except ValueError:
            self.clear_results()

    def clear_results(self):
        for mode in self.modes:
            for pre_delay_var, decay_ms_var, decay_sec_var in self.result_entries[mode]:
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