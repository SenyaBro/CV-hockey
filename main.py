"""
Запускалка: проверка окружения и версии Torch.
Пример:  python main.py
"""
import sys
print("Python:", sys.version)
try:
    import torch
    print("Torch:", torch.version, "CUDA:", torch.cuda.is_available())
except Exception as e:
    print("Torch not available:", e)
