import random

# Размеры блоков и настройки для интеграции с главным файлом
BLOCK_SIZE = 40

# Словарь доступных блоков и их параметров
BLOCK_TYPES = {
    "AIR": {"color": (50, 50, 50), "collidable": False, "name": "Воздух"},
    "GRASS": {"color": (34, 139, 34), "collidable": True, "name": "Трава"},
    "DIRT": {"color": (139, 69, 19), "collidable": True, "name": "Земля"},
    "STONE": {"color": (128, 128, 128), "collidable": True, "name": "Камень"},
    "COAL_ORE": {"color": (70, 70, 70), "collidable": True, "name": "Угольная руда"},
    "IRON_ORE": {"color": (210, 105, 30), "collidable": True, "name": "Железная руда"},
    "BEDROCK": {"color": (20, 20, 20), "collidable": True, "name": "Бедрок"}
}

class World:
    def __init__(self, size=100):
        self.size = size
        self.blocks = []
        self.generate_world()

    def generate_world(self):
        """Процедурная генерация одномерного мира с биомами и рудами."""
        self.blocks = []
        
        for i in range(self.size):
            # Границы мира защищаем бедроком, который нельзя сломать
            if i == 0 or i == self.size - 1:
                self.blocks.append("BEDROCK")
                continue

            # Генерация структуры мира на основе вероятностей
            rand = random.random()
            
            if rand < 0.15:
                # Редкие залежи железной руды
                self.blocks.append("IRON_ORE")
            elif rand < 0.35:
                # Угольная руда
                self.blocks.append("COAL_ORE")
            elif rand < 0.65:
                # Обычный камень
                self.blocks.append("STONE")
            elif rand < 0.85:
                # Земля
                self.blocks.append("DIRT")
            else:
                # Поверхностный слой травы
                self.blocks.append("GRASS")

    def get_block(self, index):
        """Получить тип блока по его индексу в мире."""
        if 0 <= index < self.size:
            return self.blocks[index]
        return "BEDROCK"

    def set_block(self, index, block_type):
        """Установить блок в определенную позицию."""
        if 0 <= index < self.size and block_type in BLOCK_TYPES:
            # Бедрок заменять нельзя
            if self.blocks[index] != "BEDROCK":
                self.blocks[index] = block_type
                return True
        return False

    def break_block(self, index):
        """Разрушить блок, превратив его в воздух. Возвращает тип добытого блока."""
        if 0 <= index < self.size:
            block_type = self.blocks[index]
            # Нельзя ломать воздух и бедрок
            if block_type != "AIR" and block_type != "BEDROCK":
                self.blocks[index] = "AIR"
                return block_type
        return None

    def place_block(self, index, block_type):
        """Поставить блок, если на этом месте сейчас воздух."""
        if 0 <= index < self.size and self.blocks[index] == "AIR":
            self.blocks[index] = block_type
            return True
        return False
