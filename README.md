# Reverb Time Calculator
Простое настольное приложение для звукоинженеров и музыкальных продюсеров. Позволяет мгновенно рассчитать параметры реверберации (Pre-delay и Decay) на основе BPM композиции.

## Основные возможности
- **Динамический расчет:** Значения обновляются в реальном времени при изменении BPM.
- **Четыре типа пространств:** Расчеты для Hall, Large Room, Small Room и Tight Ambience.
- **Точность:** Вывод результатов в миллисекундах и секундах с точностью до двух знаков после запятой.
- **Интерфейс:** Построен на базе `CustomTkinter` с использованием системных шрифтов Segoe UI (Windows) для обеспечения нативного вида.

## Стек технологий
- **Язык:** Python 3.x
- **Библиотеки интерфейса:** CustomTkinter, Tkinter
- **Сборка:** PyInstaller

## Установка и запуск из исходного кода

1. Клонируйте репозиторий:
    ```Bash
	git clone https://github.com/SmartRightHere/reverb_calc.git
	cd reverb_calc
    ```
	
2. Установите зависимости:
    Bash
    ```
	pip install -r requirements.txt
    ```
    
3. Запустите приложение:
	Bash
	```
	python main.py
	```

## Инструкция по сборке в .exe

Для создания самостоятельного исполняемого файла для Windows выполните следующую команду в терминале:

Bash
```Bash
pyinstaller --noconfirm --onefile --windowed --name "Reverb Calculator by Smart" --add-data "venv/Lib/site-packages/customtkinter;customtkinter/" --icon "icon.ico" main.py
```

_Примечание: Убедитесь, что путь в `--add-data` соответствует расположению библиотеки в вашем виртуальном окружении._
