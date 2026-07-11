import sys
import random
import pygame

# --- НАСТРОЙКИ ИГРЫ ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60

BLOCK_SIZE = 40
WORLD_SIZE = 100  # Длина одномерного мира в блоках

# Цвета блоков (RGB)
COLORS = {
    "SKY": (135, 206, 235),     # Голубое небо сверху
    "AIR": (50, 50, 50),        # Пустое пространство на линии (воздух)
    "GRASS": (34, 139, 34),     # Трава
    "DIRT": (139, 69, 19),      # Земля
    "STONE": (128, 128, 128),   # Камень
    "PLAYER": (255, 0, 0),      # Игрок (красный квадрат)
    "SELECTOR": (255, 255, 0)   # Курсор/Выбор (желтый контур)
}

class Minecraft1D:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minecraft 1D")
        self.clock = pygame.time.Clock()
        
        # --- ГЕНЕРАЦИЯ МИРА ---
        # Создаем плоский мир из разных блоков
        self.world = []
        for i in range(WORLD_SIZE):
            rand = random.random()
            if rand < 0.6:
                self.world.append("GRASS")
            elif rand < 0.9:
                self.world.append("DIRT")
            else:
                self.world.append("STONE")
                
        # --- ИГРОК ---
        self.player_pos = WORLD_SIZE // 2  # Спавн в центре мира
        self.inventory = {"GRASS": 5, "DIRT": 5, "STONE": 5}
        self.selected_block = "GRASS"
        
        # Камера (смещение отрисовки, чтобы игрок был по центру)
        self.camera_x = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                # Движение влево и вправо
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    if self.player_pos > 0:
                        self.player_pos -= 1
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    if self.player_pos < WORLD_SIZE - 1:
                        self.player_pos += 1
                        
                # Выбор блока в инвентаре (Клавиши 1, 2, 3)
                if event.key == pygame.K_1:
                    self.selected_block = "GRASS"
                if event.key == pygame.K_2:
                    self.selected_block = "DIRT"
                if event.key == pygame.K_3:
                    self.selected_block = "STONE"
                    
                # Действия: Разрушить (Пробел) или Поставить (E)
                if event.key == pygame.K_SPACE:
                    self.break_block()
                if event.key == pygame.K_e:
                    self.place_block()

    def break_block(self):
        # Ломаем блок под собой, если там что-то есть
        current_block = self.world[self.player_pos]
        if current_block != "AIR":
            self.inventory[current_block] = self.inventory.get(current_block, 0) + 1
            self.world[self.player_pos] = "AIR"
            print(f"Добыто: {current_block}. Инвентарь: {self.inventory}")

    def place_block(self):
        # Ставим блок под себя, если там пусто
        if self.world[self.player_pos] == "AIR":
            if self.inventory.get(self.selected_block, 0) > 0:
                self.world[self.player_pos] = self.selected_block
                self.inventory[self.selected_block] -= 1
                print(f"Поставлен: {self.selected_block}. Осталось: {self.inventory[self.selected_block]}")

    def update_camera(self):
        # Центрируем камеру на игроке
        target_x = self.player_pos * BLOCK_SIZE - SCREEN_WIDTH // 2
        self.camera_x += (target_x - self.camera_x) * 0.1  # Плавный скролл

    def draw(self):
        # Заливка неба
        self.screen.fill(COLORS["SKY"])
        
        # Линия земли находится по центру экрана по вертикали
        floor_y = SCREEN_HEIGHT // 2
        
        # Отрисовка блоков мира
        for i, block_type in enumerate(self.world):
            block_x = i * BLOCK_SIZE - int(self.camera_x)
            
            # Рисуем блок только если он виден на экране
            if -BLOCK_SIZE < block_x < SCREEN_WIDTH:
                rect = pygame.Rect(block_x, floor_y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, COLORS[block_type], rect)
                # Рисуем границы блока
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
                
        # Отрисовка игрока
        player_x = self.player_pos * BLOCK_SIZE - int(self.camera_x)
        player_rect = pygame.Rect(player_x, floor_y - BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(self.screen, COLORS["PLAYER"], player_rect)
        
        # Селектор под игроком (желтая рамка вокруг блока, с которым взаимодействуем)
        selector_rect = pygame.Rect(player_x, floor_y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(self.screen, COLORS["SELECTOR"], selector_rect, 3)
        
        # Вывод интерфейса (HUD)
        self.draw_hud()
        
        pygame.display.flip()

    def draw_hud(self):
        font = pygame.font.SysFont(None, 24)
        info_text = f"Выбран блок: {self.selected_block} (У вас: {self.inventory[self.selected_block]})"
        controls_text = "A/D - Ходить | ПРОБЕЛ - Ломать | E - Поставить | 1,2,3 - Выбор блока"
        
        img_info = font.render(info_text, True, (0, 0, 0))
        img_ctrl = font.render(controls_text, True, (50, 50, 50))
        
        self.screen.blit(img_info, (10, 10))
        self.screen.blit(img_ctrl, (10, 35))

    def run(self):
        while True:
            self.handle_input()
            self.update_camera()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Minecraft1D()
    game.run()
