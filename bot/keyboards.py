from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Основная клавиатура
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Расскажи мне историю кухни мира")],
        [KeyboardButton(text="Предложи мне рецепт")],
    ],
    resize_keyboard=True
)

# Клавиатура для уточнения времени приема пищи
meal_time_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Завтрак")],
        [KeyboardButton(text="Обед")],
        [KeyboardButton(text="Ужин")],
    ],
    resize_keyboard=True
)

# Клавиатура для уточнения: напиток или еда
recipe_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Блюдо")],
        [KeyboardButton(text="Напиток")],
    ],
    resize_keyboard=True
)

# Клавиатура для уточнения типа кухни
kitchen_style_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Традиционной")],
        [KeyboardButton(text="Современной")],
    ],
    resize_keyboard=True
)

# Клавиатура для уточнения о кухне мира: история или рецепт
history_or_recipe_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Историю")],
        [KeyboardButton(text="Рецепт")],
    ],
    resize_keyboard=True
)

# Клавиатура возвращения назад
move_back_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Вернуться в начало")],
        [KeyboardButton(text="Вернуться на шаг назад")],
    ],
    resize_keyboard=True
)