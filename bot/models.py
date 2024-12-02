from huggingface_hub import AsyncInferenceClient
from bot.config import LLAMA_MODEL, GPT_MODEL, HUGGINGFACE_TOKEN, LLAMA_CONFIG, GPT_CONFIG
import aiohttp
import textstat

# Инициализация асинхронного клиента Hugging Face с API ключом
client = AsyncInferenceClient(api_key=HUGGINGFACE_TOKEN)

async def readability_score(text: str) -> float:
    """
    Вычисляет индекс удобочитаемости текста по шкале Flesch Reading Ease.
    
    :param text: Текст для вычисления индекса удобочитаемости.
    :return: Оценка Flesch Reading Ease для текста.
    """
    return textstat.flesch_reading_ease(text)

async def generate_text(user_query: str) -> str:
    """
    Генерирует два текста, один с использованием модели Llama, второй с использованием GPT.
    Сравнивает их по метрике удобочитаемости и возвращает лучший текст.
    
    :param user_query: Запрос пользователя, на основе которого генерируются тексты.
    :return: Наиболее удобочитаемый текст из двух сгенерированных.
    """
    # Получаем сгенерированные тексты от моделей
    text1 = await send_request_to_llama(user_query=user_query)
    text2 = await send_request_to_gpt(query_text=user_query)
    
    # Вычисляем метрики для каждого текста
    score1 = await readability_score(text1)
    score2 = await readability_score(text2)

    # Печатаем сами тексты и их оценки
    print("Llama generated text:")
    print(text1)
    print("Flesch Reading Ease score:", score1)
    print("\nGPT generated text:")
    print(text2)
    print("Flesch Reading Ease score:", score2)

    if text1.startswith("Error:"):
        score1 = 0

    if text2.startswith("Error:"):
        score2 = 0
    
    # Сравниваем метрики и возвращаем лучший текст
    if score1 > score2:
        return "Ваш запрос: " + text1
    else:
        return "Ваш запрос: " + text2

async def send_request_to_llama(user_query: str) -> str:
    """
    Отправляет запрос к модели Llama для генерации текста.

    :param user_query: Запрос пользователя, на основе которого генерируется текст.
    :return: Сгенерированный текст от модели Llama или сообщение об ошибке.
    """
    messages = [
        {
            "role": "user",
            "content": user_query
        }
    ]
    
    try:
        completion = await client.chat.completions.create(
            model=LLAMA_MODEL, 
            messages=messages, 
            **LLAMA_CONFIG
        )
        
        # Извлекаем текст из ответа
        return completion.choices[0].message['content']
    except Exception as e:
        return f"Error: {str(e)}"

headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

async def send_request_to_gpt(query_text: str) -> str:
    """
    Отправляет запрос к модели GPT для генерации текста.

    :param query_text: Запрос пользователя, на основе которого генерируется текст.
    :return: Сгенерированный текст от модели GPT или сообщение об ошибке.
    """
    payload = {
        "inputs": query_text,
        "parameters": GPT_CONFIG,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(GPT_MODEL, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return result[0].get('generated_text', '')
                else:
                    return f"Error: Request failed with status code {response.status}"
        except aiohttp.ClientError as e:
            return f"Error: {str(e)}"
