import os
import subprocess
import sys

def check_and_install_dependencies():
    """Проверяет наличие pygame и устанавливает его, если нужно."""
    print("[1/3] Проверка библиотек...")
    try:
        import pygame
        print(" -> [OK] Библиотека Pygame уже установлена.")
    except ImportError:
        print(" -> [!] Pygame не найден. Устанавливаю через pip...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
            print(" -> [OK] Pygame успешно установлен!")
        except Exception as e:
            print(f" -> [ОШИБКА] Не удалось установить Pygame: {e}")
            print("Попробуйте вручную выполнить команду: pip install pygame")
            sys.exit(1)

def ensure_assets_exist():
    """Проверяет наличие текстур и запускает генератор, если их нет."""
    print("[2/3] Проверка игровых ресурсов...")
    target_texture = os.path.join("assets", "textures", "grass.png")
    
    if not os.path.exists(target_texture):
        print(" -> [!] Текстуры не найдены. Запуск генерации...")
        
        # Ищем доступный скрипт генерации
        if os.path.exists("generate_assets.py"):
            subprocess.run([sys.executable, "generate_assets.py"])
        elif os.path.exists("generate_sprites.py"):
            subprocess.run([sys.executable, "generate_sprites.py"])
        else:
            print(" -> [ПРЕДУПРЕЖДЕНИЕ] Скрипты генерации ресурсов не найдены.")
            print(" Игра может запуститься без текстур или вылететь.")
            return
        print(" -> [OK] Ресурсы успешно сгенерированы.")
    else:
        print(" -> [OK] Текстуры и звуки на месте.")

def start_game():
    """Запускает главный файл игры main.py."""
    print("[3/3] Инициализация игрового движка...")
    print("-" * 50)
    
    if os.path.exists("main.py"):
        # Запускаем main.py в текущем окружении
        subprocess.run([sys.executable, "main.py"])
    else:
        print("[ОШИБКА] Файл main.py не найден в текущей директории!")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 50)
    print("  Универсальный лончер Minecraft 1D ⛏️")
    print("=" * 50)
    
    check_and_install_dependencies()
    print()
    ensure_assets_exist()
    print()
    start_game()
