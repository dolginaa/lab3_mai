import os

# Токены
BOT_TOKEN = os.getenv("BOT_TOKEN", "7595427949:AAH4WAJYOVwh8iNKd53KchZOaiVG1avBZ3k")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "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")

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
