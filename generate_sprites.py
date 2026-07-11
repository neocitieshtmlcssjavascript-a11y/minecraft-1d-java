import os
import pygame

def create_sprites():
    pygame.init()
    
    # Создаем папку sprites, если её нет
    if not os.path.exists("sprites"):
        os.makedirs("sprites")
        
    size = (40, 40)
    
    # 1. ТРАВА (GRASS)
    grass = pygame.Surface(size)
    grass.fill((139, 69, 19)) # Земляная основа
    pygame.draw.rect(grass, (34, 139, 34), (0, 0, 40, 12)) # Верхняя зелень
    pygame.draw.rect(grass, (50, 205, 5), (4, 12, 4, 6))  # Пиксели травы вниз
    pygame.draw.rect(grass, (50, 205, 5), (20, 12, 4, 4))
    pygame.draw.rect(grass, (50, 205, 5), (32, 12, 4, 8))
    pygame.image.save(grass, "sprites/grass.png")

    # 2. ЗЕМЛЯ (DIRT)
    dirt = pygame.Surface(size)
    dirt.fill((139, 69, 19))
    # Добавляем темные пиксели для текстуры земли
    dark_brown = (100, 50, 15)
    pygame.draw.rect(dirt, dark_brown, (4, 4, 4, 4))
    pygame.draw.rect(dirt, dark_brown, (24, 12, 4, 4))
    pygame.draw.rect(dirt, dark_brown, (12, 28, 4, 4))
    pygame.draw.rect(dirt, dark_brown, (28, 24, 4, 4))
    pygame.image.save(dirt, "sprites/dirt.png")

    # 3. КАМЕНЬ (STONE)
    stone = pygame.Surface(size)
    stone.fill((128, 128, 128))
    # Текстурные трещины на камне
    dark_gray = (90, 90, 90)
    pygame.draw.rect(stone, dark_gray, (0, 8, 12, 4))
    pygame.draw.rect(stone, dark_gray, (12, 12, 4, 12))
    pygame.draw.rect(stone, dark_gray, (24, 28, 16, 4))
    pygame.image.save(stone, "sprites/stone.png")

    # 4. УГОЛЬНАЯ РУДА (COAL_ORE)
    coal = pygame.Surface(size)
    coal.fill((128, 128, 128)) # Каменная основа
    # Черные вкрапления угля
    black = (40, 40, 40)
    pygame.draw.rect(coal, black, (8, 8, 8, 4))
    pygame.draw.rect(coal, black, (24, 12, 4, 8))
    pygame.draw.rect(coal, black, (12, 24, 8, 8))
    pygame.image.save(coal, "sprites/coal_ore.png")

    # 5. ЖЕЛЕЗНАЯ РУДА (IRON_ORE)
    iron = pygame.Surface(size)
    iron.fill((128, 128, 128))
    # Оранжево-бежевые вкрапления железа
    orange = (210, 105, 30)
    pygame.draw.rect(iron, orange, (4, 12, 8, 4))
    pygame.draw.rect(iron, orange, (20, 4, 4, 8))
    pygame.draw.rect(iron, orange, (24, 24, 12, 4))
    pygame.image.save(iron, "sprites/iron_ore.png")

    # 6. БЕДРОК (BEDROCK)
    bedrock = pygame.Surface(size)
    bedrock.fill((40, 40, 40))
    # Хаотичные темные пятна неразрушимой породы
    v_dark = (20, 20, 20)
    pygame.draw.rect(bedrock, v_dark, (0, 0, 16, 16))
    pygame.draw.rect(bedrock, v_dark, (20, 16, 16, 16))
    pygame.draw.rect(bedrock, v_dark, (4, 32, 12, 8))
    pygame.image.save(bedrock, "sprites/bedrock.png")

    # 7. ИГРОК (PLAYER)
    player = pygame.Surface(size, pygame.SRCALPHA) # Прозрачный фон вокруг скина
    # Голова (цвет кожи)
    pygame.draw.rect(player, (255, 220, 180), (12, 0, 16, 16))
    # Глаза
    pygame.draw.rect(player, (0, 0, 255), (16, 4, 4, 4))
    pygame.draw.rect(player, (0, 0, 255), (24, 4, 4, 4))
    # Тело (Синяя футболка Стива)
    pygame.draw.rect(player, (0, 150, 255), (8, 16, 24, 16))
    # Штаны (Фиолетовые)
    pygame.draw.rect(player, (100, 0, 150), (10, 32, 20, 8))
    pygame.image.save(player, "sprites/player.png")

    print("✅ Все спрайты успешно созданы и сохранены в папку 'sprites/'!")

if __name__ == "__main__":
    create_sprites()
