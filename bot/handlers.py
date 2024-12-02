from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards import main_menu_keyboard, move_back_keyboard, meal_time_keyboard, recipe_type_keyboard, kitchen_style_keyboard, history_or_recipe_keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.models import generate_text

# Создание маршрутизатора
router = Router()

# Переменная для хранения выбора пользователя
user_choices = {}

# Стейт ожидания пользовательского ввода вида кухни мира
class CuisineStates(StatesGroup):
    waiting_for_cuisine = State()


# Стейт ожидания пользовательского ввода ингредиента
class RecipeStates(StatesGroup):
    waiting_for_ingredient = State()


# Обработчик команды /start
@router.message(Command("start"))
async def start_handler(message: Message):
    """
    Обрабатывает команду /start. Инициализирует выбор пользователя и отправляет приветственное сообщение с основным меню.
    
    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message    
    """
    user_choices[message.from_user.id] = {}

    await message.answer(
        "Привет! Я твой кулинарный помощник. Выбери, что ты хочешь сделать:",
        reply_markup=main_menu_keyboard
    )


# Обработчик кнопки "Предложи мне рецепт"
@router.message(lambda message: message.text == "Предложи мне рецепт")
async def suggest_recipe_handler(message: Message):
    """
    Обрабатывает нажатие кнопки "Предложи мне рецепт". Запрашивает выбор времени приема пищи.
    
    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    """
    user_choices[message.from_user.id]["info_type"] = "recipe"
    await message.answer(
        "Выберите время приема пищи:",
        reply_markup=meal_time_keyboard
    )


# Обработчик кнопок "Завтрак", "Обед", "Ужин"
@router.message(lambda message: message.text in ["Завтрак", "Обед", "Ужин"])
async def meal_time_handler(message: Message):
    """
    Обрабатывает выбор времени приема пищи (Завтрак, Обед, Ужин). Запрашивает тип рецепта.
    
    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    """
    if message.from_user.id in user_choices:
        user_choices[message.from_user.id]["meal_time"] = message.text
    await message.answer(
        "Хорошо. Теперь выберите тип рецепта, который вы хотите получить: рецепт напитка или рецепт блюда.",
        reply_markup=recipe_type_keyboard
    )


# Обработчик кнопок "Напиток" и "Блюдо"
@router.message(lambda message: message.text in ["Напиток", "Блюдо"])
async def recipe_type_handler(message: Message, state: FSMContext):
    """
    Обрабатывает выбор типа рецепта (Напиток или Блюдо). Запрашивает ингредиент.
    
    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    """
    if message.from_user.id in user_choices:
        user_choices[message.from_user.id]["recipe_type"] = message.text
    
    await message.answer("Теперь введите ингредиент, который вы хотите использовать.")

    # Переключаем пользователя в состояние ожидания ингредиента
    await state.set_state(RecipeStates.waiting_for_ingredient)


# Ждем пользовательский ввод (ингредиент)
@router.message(RecipeStates.waiting_for_ingredient)
async def ingredient_handler(msg: Message, state: FSMContext):
    """
    Обрабатывает пользовательский ввод ингредиента. Генерирует рецепт на основе выбранных данных.
    
    :param msg: Сообщение от пользователя.
    :type msg: aiogram.types.Message
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    """
    if msg.from_user.id in user_choices:
        user_choices[msg.from_user.id]["ingredient"] = msg.text

    meal_time = user_choices[msg.from_user.id].get("meal_time", "неизвестное время")
    recipe_type = user_choices[msg.from_user.id].get("recipe_type", "неизвестный тип")
    ingredient = user_choices[msg.from_user.id].get("ingredient", "неизвестный ингредиент")

    generated_test = await generate_text(f"Предложи мне рецепт. Я хочу приготовить что-то на {meal_time.lower()}. Я хочу чтобы это был рецепт {recipe_type.lower()}. У меня уже есть один ингредиент: {ingredient}. \nРецепт: ")
    await msg.answer(
        generated_test,
        reply_markup=move_back_keyboard
    )

    # Заканчиваем состояние
    await state.clear()


# Обработчик кнопки "Расскажи мне историю кухни мира"
@router.message(lambda message: message.text == "Расскажи мне историю кухни мира")
async def tell_kitchen_story_handler(message: Message):
    """
    Обрабатывает нажатие кнопки "Расскажи мне историю кухни мира". Запрашивает тип интерпретации кухни.
    
    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    """
    user_choices[message.from_user.id]["info_type"] = "cuisine"

    await message.answer(
        "Вы хотели бы узнать о традиционной или современной интерпретации?",
        reply_markup=kitchen_style_keyboard
    )


# Обработчик выбора типа кухни
@router.message(lambda message: message.text in ["Традиционной", "Современной"])
async def kitchen_style_handler(message: Message):
    """
    Обрабатывает выбор типа кухни (Традиционной или Современной). Запрашивает дальнейший выбор информации.
    
    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    """
    if message.from_user.id in user_choices:
        user_choices[message.from_user.id]["cuisine_type"] = message.text
    await message.answer(
        "Хорошо. Теперь выберите какую информацию вы хотите получить: рецепт или историю.",
        reply_markup=history_or_recipe_keyboard
    )


# Обработчик кнопок "Рецепт" и "Историю"
@router.message(lambda message: message.text in ["Рецепт", "Историю"])
async def recipe_type_handler(message: Message, state: FSMContext):
    """
    Обрабатывает выбор типа информации (Рецепт или Историю). Запрашивает название кухни.
    
    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    """
    if message.from_user.id in user_choices:
        user_choices[message.from_user.id]["cuisine_info_type"] = message.text
    
    await message.answer("Теперь введите название кухни, о которой вы хотели бы узнать.")

    # Переключаем пользователя в состояние ожидания кухни
    await state.set_state(CuisineStates.waiting_for_cuisine)


# Ждем пользовательский ввод (название кухни)
@router.message(CuisineStates.waiting_for_cuisine)
async def cuisine_handler(msg: Message, state: FSMContext):
    """
    Обрабатывает пользовательский ввод названия кухни. Генерирует запрос о кухне мира.
    
    :param msg: Сообщение от пользователя.
    :type msg: aiogram.types.Message
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    """
    if msg.from_user.id in user_choices:
        user_choices[msg.from_user.id]["cuisine"] = msg.text

    cuisine_type = user_choices[msg.from_user.id].get("cuisine_type", "неизвестное время")
    cuisine_info_type = user_choices[msg.from_user.id].get("cuisine_info_type", "неизвестный тип")
    cuisine = user_choices[msg.from_user.id].get("cuisine", "неизвестный ингредиент")

    generated_test = await generate_text(f"Расскажи о кухне мира. Я бы хотела знать о {cuisine_type.lower()} представлении такой кухни как {cuisine}. А конкретно я бы хотела узнать {cuisine_info_type.lower()} этой кухни. \nРезультат: ")
    await msg.answer(
        generated_test,
        reply_markup=move_back_keyboard
    )

    # Заканчиваем состояние
    await state.clear()


# Обработчики кнопок перемещения в начало
@router.message(lambda message: message.text == "Вернуться в начало")
async def move_to_beginning_handler(message: Message):
    """
    Обрабатывает кнопку "Вернуться в начало". Инициализирует выбор пользователя заново.
    
    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    """
    user_choices[message.from_user.id] = {}

    await message.answer(
        "Привет! Я твой кулинарный помощник. Выбери, что ты хочешь сделать:",
        reply_markup=main_menu_keyboard
    )

@router.message(lambda message: message.text == "Вернуться на шаг назад")
async def move_back_handler(message: Message, state: FSMContext) -> None:
    """
    Обработчик кнопки "Вернуться на шаг назад". В зависимости от выбранного пользователем типа информации
    (рецепт или кухня), переводит пользователя в соответствующее состояние для ввода ингредиента или кухни.

    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    :param state: Состояние FSM.
    :type state: aiogram.fsm.context.FSMContext
    """
    if user_choices[message.from_user.id]["info_type"] is not None and \
        user_choices[message.from_user.id]["info_type"] == "recipe":
        await message.answer("Теперь введите ингредиент, который вы хотите использовать.")
        await state.set_state(RecipeStates.waiting_for_ingredient)
    elif user_choices[message.from_user.id]["info_type"] is not None and \
        user_choices[message.from_user.id]["info_type"] == "cuisine":
        await message.answer("Теперь введите название кухни, о которой вы хотели бы узнать.")
        await state.set_state(CuisineStates.waiting_for_cuisine)


# Обработчик неизвестных сообщений
@router.message()
async def unknown_handler(message: Message) -> None:
    """
    Обработчик для неизвестных сообщений. Отправляет пользователю сообщение о том, что он должен выбрать
    один из доступных вариантов меню.

    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    """
    await message.answer("Пожалуйста, выберите один из доступных вариантов меню.")
