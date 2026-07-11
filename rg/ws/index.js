// --- КОНСТАНТЫ И НАСТРОЙКИ ---
const BLOCK_SIZE = 40;
const WORLD_SIZE = 100;

const BLOCK_TYPES = {
    "AIR": { color: "#323232", name: "Воздух", mineable: false },
    "GRASS": { color: "#228B22", name: "Трава", mineable: true },
    "DIRT": { color: "#8B4513", name: "Земля", mineable: true },
    "STONE": { color: "#808080", name: "Камень", mineable: true },
    "COAL_ORE": { color: "#464646", name: "Угольная руда", mineable: true },
    "IRON_ORE": { color: "#D2691E", name: "Железная руда", mineable: true },
    "BEDROCK": { color: "#141414", name: "Бедрок", mineable: false }
};

// --- КЛАСС МИРА ---
class World {
    constructor(size) {
        this.size = size;
        this.blocks = [];
        this.generate();
    }

    generate() {
        for (let i = 0; i < this.size; i++) {
            if (i === 0 || i === this.size - 1) {
                this.blocks.push("BEDROCK");
                continue;
            }
            const rand = Math.random();
            if (rand < 0.15) this.blocks.push("IRON_ORE");
            else if (rand < 0.35) this.blocks.push("COAL_ORE");
            else if (rand < 0.65) this.blocks.push("STONE");
            else if (rand < 0.85) this.blocks.push("DIRT");
            else this.blocks.push("GRASS");
        }
    }

    getBlock(index) {
        return this.blocks[index] || "BEDROCK";
    }

    breakBlock(index) {
        const blockType = this.blocks[index];
        if (blockType && blockType !== "AIR" && BLOCK_TYPES[blockType].mineable) {
            this.blocks[index] = "AIR";
            return blockType;
        }
        return null;
    }

    placeBlock(index, blockType) {
        if (this.blocks[index] === "AIR") {
            this.blocks[index] = blockType;
            return true;
        }
        return false;
    }
}

// --- КЛАСС ИГРОКА ---
class Player {
    constructor(startPos) {
        this.posX = startPos;
        this.hp = 10;
        this.inventory = { "GRASS": 10, "DIRT": 10, "STONE": 5, "COAL_ORE": 0, "IRON_ORE": 0 };
        this.hotbar = ["GRASS", "DIRT", "STONE", "COAL_ORE", "IRON_ORE"];
        this.selectedIndex = 0;
    }

    get selectedBlock() {
        return this.hotbar[this.selectedIndex];
    }

    move(dir, worldSize) {
        const newPos = this.posX + dir;
        if (newPos > 0 && newPos < worldSize - 1) {
            this.posX = newPos;
        }
    }

    selectSlot(index) {
        if (index >= 0 && index < this.hotbar.length) {
            this.selectedIndex = index;
        }
    }
}

// --- КЛАСС ИГРОВОГО ДВИЖКА ---
class Game {
    constructor() {
        this.canvas = document.getElementById("gameCanvas");
        this.ctx = this.canvas.getContext("2d");
        this.floorY = this.canvas.height / 2;

        this.world = new World(WORLD_SIZE);
        this.player = new Player(Math.floor(WORLD_SIZE / 2));
        this.cameraX = this.player.posX * BLOCK_SIZE - this.canvas.width / 2;

        this.initInput();
        this.loop();
    }

    // Взаимодействие со звуковым движком браузера
    playSound(freq, type, duration) {
        try {
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();

            oscillator.type = type;
            oscillator.frequency.setValueAtTime(freq, audioCtx.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + duration);

            gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);

            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);

            oscillator.start();
            oscillator.stop(audioCtx.currentTime + duration);
        } catch (e) {
            // Браузеры могут блокировать звук до первого клика по экрану
        }
    }

    initInput() {
        window.addEventListener("keydown", (e) => {
            switch(e.code) {
                case "KeyA": case "ArrowLeft": this.player.move(-1, this.world.size); break;
                case "KeyD": case "ArrowRight": this.player.move(1, this.world.size); break;
                case "Space": 
                    const mined = this.world.breakBlock(this.player.posX);
                    if (mined) {
                        this.player.inventory[mined] = (this.player.inventory[mined] || 0) + 1;
                        this.playSound(140, "square", 0.12);
                    }
                    e.preventDefault(); 
                    break;
                case "KeyE": 
                    const block = this.player.selectedBlock;
                    if (this.player.inventory[block] > 0) {
                        const success = this.world.placeBlock(this.player.posX, block);
                        if (success) {
                            this.player.inventory[block]--;
                            this.playSound(280, "triangle", 0.08);
                        }
                    }
                    break;
                case "Digit1": this.player.selectSlot(0); break;
                case "Digit2": this.player.selectSlot(1); break;
                case "Digit3": this.player.selectSlot(2); break;
                case "Digit4": this.player.selectSlot(3); break;
                case "Digit5": this.player.selectSlot(4); break;
            }
        });
    }

    updateCamera() {
        const targetCameraX = this.player.posX * BLOCK_SIZE - this.canvas.width / 2;
        this.cameraX += (targetCameraX - this.cameraX) * 0.1;
    }

    draw() {
        // Очистка неба
        this.ctx.fillStyle = "#87CEEB";
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Отрисовка мира с учетом камеры
        for (let i = 0; i < this.world.size; i++) {
            const blockType = this.world.getBlock(i);
            const blockX = i * BLOCK_SIZE - Math.floor(this.cameraX);

            if (blockX > -BLOCK_SIZE && blockX < this.canvas.width) {
                this.ctx.fillStyle = BLOCK_TYPES[blockType].color;
                this.ctx.fillRect(blockX, this.floorY, BLOCK_SIZE, BLOCK_SIZE);
                
                this.ctx.strokeStyle = "rgba(0, 0, 0, 0.15)";
                this.ctx.lineWidth = 1;
                this.ctx.strokeRect(blockX, this.floorY, BLOCK_SIZE, BLOCK_SIZE);
            }
        }

        // Отрисовка игрока
        const playerX = this.player.posX * BLOCK_SIZE - Math.floor(this.cameraX);
        
        this.ctx.fillStyle = "#FFDCB4"; // Голова
        this.ctx.fillRect(playerX + 12, this.floorY - BLOCK_SIZE, 16, 16);
        this.ctx.fillStyle = "#0000FF"; // Глаза
        this.ctx.fillRect(playerX + 16, this.floorY - BLOCK_SIZE + 4, 4, 4);
        this.ctx.fillRect(playerX + 24, this.floorY - BLOCK_SIZE + 4, 4, 4);
        this.ctx.fillStyle = "#0096FF"; // Рубашка
        this.ctx.fillRect(playerX + 8, this.floorY - BLOCK_SIZE + 16, 24, 16);
        this.ctx.fillStyle = "#640096"; // Штаны
        this.ctx.fillRect(playerX + 10, this.floorY - BLOCK_SIZE + 32, 20, 8);

        // Желтая рамка-селектор
        this.ctx.strokeStyle = "#FFFF00";
        this.ctx.lineWidth = 3;
        this.ctx.strokeRect(playerX, this.floorY, BLOCK_SIZE, BLOCK_SIZE);

        this.drawHUD();
    }

    drawHUD() {
        this.ctx.fillStyle = "#000000";
        this.ctx.font = "16px 'Courier New'";

        const hearts = "❤️".repeat(this.player.hp);
        this.ctx.fillText(`HP: ${hearts}`, 15, 30);

        const activeBlock = this.player.selectedBlock;
        const count = this.player.inventory[activeBlock] || 0;
        
        this.ctx.fillStyle = "#fff";
        this.ctx.shadowColor = "black";
        this.ctx.shadowBlur = 4;
        this.ctx.fillText(`Выбран блок: ${BLOCK_TYPES[activeBlock].name} (${count} шт.)`, 15, 60);
        this.ctx.shadowBlur = 0;
    }

    loop() {
        this.updateCamera();
        this.draw();
        requestAnimationFrame(() => this.loop());
    }
}

// Запуск игры после загрузки страницы
window.onload = () => {
    new Game();
};
