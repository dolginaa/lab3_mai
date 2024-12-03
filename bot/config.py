import os

# Токены

# Модели
LLAMA_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
GPT_MODEL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neox-20b"

# Конфигурация моделей
LLAMA_CONFIG = {
    "top_p": 0.7,
    "temperature": 0.3,
    "max_tokens": 250,
}

GPT_CONFIG = {
    "top_p": 0.6,
    "top_k": 50,
    "temperature": 0.5,
    "repetition_penalty": 2.0,
    "min_length": 70,
    # "max_tokens": 250,  # если понадобится
}
