@echo off
:: Установка кодировки UTF-8 для корректного отображения кириллицы в консоли
chcp 65001 > nul

title Minecraft 1D - Запуск игры ⛏️

echo ===================================================
echo   Запуск Minecraft 1D...
echo ===================================================
echo.

:: 1. Проверка, установлены ли зависимости из requirements.txt
echo [1/3] Проверка библиотек...
pip show pygame >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Pygame не найден. Устанавливаю зависимости...
    pip install -r requirements.txt
) else (
    echo [OK] Все необходимые библиотеки установлены.
)
echo.

:: 2. Проверка и автоматическая генерация ассетов/спрайтов
echo [2/3] Проверка игровых ресурсов...
if not exist "assets\textures\grass.png" (
    echo [!] Текстуры не найдены. Запускаю генератор ассетов...
    if exist "generate_assets.py" (
        python generate_assets.py
    ) else if exist "generate_sprites.py" (
        python generate_sprites.py
    ) else (
        echo [ОШИБКА] Скрипт генерации ресурсов не найден!
    )
) else (
    echo [OK] Спрайты и звуки на месте.
)
echo.

:: 3. Запуск главного файла игры
echo [3/3] Инициализация игрового движка...
echo.
python main.py

:: Если игра завершилась с ошибкой, консоль не закроется сразу
if %errorlevel% neq 0 (
    echo.
    echo ===================================================
    echo [ОШИБКА] Игра завершилась некорректно.
    echo Проверьте текст ошибки выше.
    echo ===================================================
    pause
)
