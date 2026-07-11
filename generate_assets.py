import os
import math
import wave
import struct

def create_folders():
    paths = [
        "assets/textures",
        "assets/sounds",
        "assets/fonts"
    ]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Создана папка: {path}")

def generate_synth_wav(filename, duration=0.15, start_freq=200, end_freq=80, type_wave="square"):
    """Генерирует звуковой 8-битный эффект (чиптюн) и сохраняет в WAV."""
    sample_rate = 11025
    num_samples = int(duration * sample_rate)
    
    with wave.open(filename, 'w') as wav_file:
        # Моно, 1 байт на семпл (8 бит), частота дискретизации
        wav_file.setparams((1, 1, sample_rate, num_samples, 'NONE', 'not compressed'))
        
        data = bytearray()
        for i in range(num_samples):
            # Плавное изменение частоты (глайд)
            t = i / num_samples
            current_freq = start_freq + (end_index := (end_freq - start_freq) * t)
            
            # Генерация фазы волны
            phase = (2 * math.pi * current_freq * (i / sample_rate))
            
            if type_wave == "square":
                # Меандр (квадратная волна) для ретро-звука разрушения
                value = 127 if math.sin(phase) >= 0 else -128
            elif type_wave == "noise":
                # Псевдо-шум для глухого звука земли
                value = int(127 * math.sin(phase) * math.sin(phase * 1.5))
            else:
                # Синусоида
                value = int(127 * math.sin(phase))
                
            # Затухание звука к концу
            fade = 1.0 - t
            value = int(value * fade)
            
            # Смещение из диапазона [-128, 127] в [0, 255] для 8-битного WAV
            data.append(value + 128)
            
        wav_file.writeframes(data)
    print(f"Сгенерирован звук: {filename}")

if __name__ == "__main__":
    create_folders()
    
    # Генерируем аудиоэффекты
    generate_synth_wav("assets/sounds/break.wav", duration=0.1, start_freq=150, end_freq=40, type_wave="square")
    generate_synth_wav("assets/sounds/place.wav", duration=0.08, start_freq=300, end_freq=200, type_wave="noise")
    generate_synth_wav("assets/sounds/hit.wav", duration=0.2, start_freq=100, end_freq=300, type_wave="sine")
    
    print("\n💡 Для полной интеграции перенесите ваши .png текстуры из 'sprites/' в 'assets/textures/'")
