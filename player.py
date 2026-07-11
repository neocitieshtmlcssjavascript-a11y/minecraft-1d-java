from world import BLOCK_SIZE

class Player:
    def __init__(self, start_pos):
        # Позиция игрока в координатах блоков мира
        self.pos_x = start_pos
        
        # Характеристики персонажа
        self.max_hp = 10
        self.hp = self.max_hp
        
        # Инвентарь: тип_блока -> количество
        self.inventory = {
            "GRASS": 10,
            "DIRT": 10,
            "STONE": 5,
            "COAL_ORE": 0,
            "IRON_ORE": 0
        }
        
        # Список доступных блоков для выбора (горячая панель / хотбар)
        self.hotbar = ["GRASS", "DIRT", "STONE", "COAL_ORE", "IRON_ORE"]
        self.selected_index = 0  # Текущий выбранный индекс в хотбаре

    @property
    def selected_block(self):
        """Возвращает название текущего выбранного блока."""
        return self.hotbar[self.selected_index]

    def move(self, direction, world_size):
        """Перемещение игрока влево (-1) или вправо (1)."""
        new_pos = self.pos_x + direction
        # Ограничиваем движение границами мира (не заходим на крайний бедрок)
        if 0 < new_pos < world_size - 1:
            self.pos_x = new_pos
            return True
        return False

    def select_slot(self, slot_index):
        """Переключение активного слота в хотбаре (от 0 до 4)."""
        if 0 <= slot_index < len(self.hotbar):
            self.selected_index = slot_index

    def add_to_inventory(self, block_type):
        """Добавление добытого блока в инвентарь."""
        if block_type:
            if block_type in self.inventory:
                self.inventory[block_type] += 1
            else:
                self.inventory[block_type] = 1

    def remove_from_inventory(self, block_type):
        """Удаление блока из инвентаря при строительстве.
        Возвращает True, если блок был успешно удален."""
        if self.inventory.get(block_type, 0) > 0:
            self.inventory[block_type] -= 1
            return True
        return False

    def take_damage(self, amount):
        """Получение урона (например, от будущих мобов)."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        """Восстановление здоровья."""
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def is_alive(self):
        """Проверка, жив ли игрок."""
        return self.hp > 0
