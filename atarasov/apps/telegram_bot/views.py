import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import telebot
import logging
import random
from django.http import HttpResponse
from functools import wraps
from datetime import datetime
from pytz import timezone, utc

# ---------------------------------------------
# Создание бота + токен                       -
# ---------------------------------------------
# https://api.telegram.org/bot<TOKEN>/setwebhook?url=https://atarasov.ru/bot/<TOKEN>/
from apps.twitch_api.api import TwitchStartPointApi

TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(TOKEN)
log = logging.getLogger(__name__)

# ---------------------------------------------
# Основная клавиатура                         -
# ---------------------------------------------
KEYBOARD = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
KEYBOARD.add(
    telebot.types.KeyboardButton('/help'),
    telebot.types.KeyboardButton('/subscriptions'),
)


# ---------------------------------------------
# Переменная со списком доступных команд      -
# ---------------------------------------------
COMMANDS = {'/start': 'Начало',
            '/help': 'Помощь по всем командам',
            '/settings': 'Настройка личных данных',
            '/subscriptions': 'Управление подписками',
            '/weather': 'Погода в Москве',
            '/schedule': 'Расписание одной группы',
            '/story': 'Увлекательные случайные истории!',
            '/newfilms': 'Новые фильмы',
            }


# ---------------------------------------------
# Вход бота                                   -
# Основная вьюшка для бота                    -
# ---------------------------------------------
@csrf_exempt
def bot_view(request):
    if 'CONTENT_TYPE' in request.META and request.META['CONTENT_TYPE'] == 'application/json':
        json_string = request.body.decode("utf-8")
        # log.info(json_string)
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_messages([update.message])
    return HttpResponse(status=200)


# ---------------------------------------------
# Декоратор                                   -
# Запрещает доступ обычным пользователям      -
# ---------------------------------------------
def admin_only(func):
    @wraps(func)
    def wrapper(message):
        if message.from_user.id == 180469947:
            func(message)
        else:
            answer = '❌❌❌\n*У Вас нет доступа!* Обратитесь к `администратору`.\n❌❌❌'
            log.info(f'{message.from_user.id}:[{message.from_user.first_name} {message.from_user.last_name}|{message.from_user.language_code}] - ОТКАЗАНО В ДОСТУПЕ!')
            debug_message_to_me(message, answer)
            bot.send_message(message.chat.id,
                             answer,
                             parse_mode="Markdown",
                             reply_markup=KEYBOARD)
    return wrapper


# ---------------------------------------------
# /help                                       -
# Помощь пользователю                         -
# ---------------------------------------------
@bot.message_handler(regexp='/help|умеешь')
def help_messages(message):
    answer = ''
    # for command, hint in COMMANDS.items():
    #     answer += f'{command} - {hint}\n'
    answer += f'НИЧЕГО НЕ РАБОТАЕТ\nПОКА'

    debug_message_to_me(message, answer)
    log.info(str(message.from_user.id) + ': ' + message.text)
    bot.send_message(message.chat.id,
                     answer, reply_markup=KEYBOARD)


# ---------------------------------------------
# /start                                      -
# Старт пользования ботом                     -
# ---------------------------------------------
@bot.message_handler(regexp='^/start$')
def start_messages(message):
    answer = f"Приветствую, `{message.from_user.first_name}`!\nЯ Бот - Помощник." \
             f"\nМогу отвечать на некоторые фразы и умею выполнять некоторые команды.\n" \
             f"Наберите /help для получения списка команд."
    # TelegramUser.objects.get_or_create(id=message.from_user.id)
    debug_message_to_me(message, answer)

    bot.send_message(message.chat.id,
                     answer,
                     parse_mode="markdown",
                     reply_markup=KEYBOARD)

@bot.message_handler(regexp='^/subscriptions$')
@admin_only
def twitch_subscribes(message):
    API = TwitchStartPointApi(token=settings.TWITCH_TOKEN)
    subscriptions = API.webhooks.subscriptions()

    answer = ''
    for stream in subscriptions:
        user_id = stream['topic'].split('=')[1]
        streamer_name = API.users(id=user_id)[0]['login']
        expires_at = stream['expires_at']
        utc_dt = datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%SZ")
        date_for_russians = utc_dt.replace(tzinfo=utc).astimezone(tz=timezone(settings.TIME_ZONE)).strftime("%d.%m.%Y %H:%M")
        answer += f'Стример {streamer_name}, подписка истекает: {date_for_russians}\n'
    log.info(answer)
    debug_message_to_me(message, answer)
    bot.send_message(message.chat.id,
                     str(answer),
                     parse_mode="html",
                     reply_markup=KEYBOARD)



@bot.message_handler(regexp='^(/subscribe \S*|sub \S*)$')
@admin_only
def twitch_subscribes(message):
    streamer_name = message.text.split(' ')[1]
    API = TwitchStartPointApi(token=settings.TWITCH_TOKEN)
    streamer_id = API.users(login=streamer_name)[0]['id']

    headers = {"Authorization": "Bearer " + settings.TWITCH_TOKEN}
    data = requests.post('https://api.twitch.tv/helix/webhooks/hub',
                         headers=headers,
                         data = {'hub.callback':"https://atarasov.ru/twitch_api/",
                                 'hub.mode': 'subscribe',
                                 'hub.lease_seconds': '864000',
                                 'hub.topic': f'https://api.twitch.tv/helix/streams?user_id={streamer_id}'})
    answer = f'{message.from_user.first_name}, Вы успешно подписались на {streamer_name}!'
    log.info(answer)
    debug_message_to_me(message, answer)
    bot.send_message(message.chat.id,
                     answer,
                     parse_mode="html",
                     reply_markup=KEYBOARD)

# ---------------------------------------------
# Функция выводящая курс валют                -
# ---------------------------------------------
# @bot.message_handler(regexp='(курс валют)')
# def get_money_messages(message):
#     try:
#         target_url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req="
#
#         today_date = '{:02d}/{:02d}/{:04d}'.format(datetime.datetime.now().day, datetime.datetime.now().month,
#                                                    datetime.datetime.now().year)
#         yesterday_date = '{:02d}/{:02d}/{:04d}'.format((datetime.datetime.today() - datetime.timedelta(days=1)).day,
#                                                        (datetime.datetime.today() - datetime.timedelta(days=1)).month,
#                                                        (datetime.datetime.today() - datetime.timedelta(days=1)).year)
#
#         request_date_today = requests.get(target_url + today_date)
#         request_date_yesterday = requests.get(target_url + yesterday_date)
#
#         tree_today = ElementTree.fromstring(request_date_today.content)
#         tree_yesterday = ElementTree.fromstring(request_date_yesterday.content)
#         # смотрим вчерашний курс валют
#         USD_yesterday = None
#         EUR_yesterday = None
#         for item in tree_yesterday:
#             if item[1].text == 'USD':
#                 USD_yesterday = item[4].text
#             if item[1].text == 'EUR':
#                 EUR_yesterday = item[4].text
#         # смотрим сегодняшний курс валют
#         USD_today = None
#         EUR_today = None
#         for item in tree_today:
#             if item[1].text == 'USD':
#                 USD_today = item[4].text
#             if item[1].text == 'EUR':
#                 EUR_today = item[4].text
#         # Разница в курсе валют
#         USD_difference = float(USD_today.replace(",", ".")) - float(USD_yesterday.replace(",", "."))
#         EUR_difference = float(EUR_today.replace(",", ".")) - float(EUR_yesterday.replace(",", "."))
#         # Вывод курса валют
#         answer = '📈Курс валют на сегодня:\n\n'
#         if USD_difference == 0:
#             answer += "Доллар США($) - " + USD_today + "\n"
#         elif USD_difference < 0:
#             answer += "Доллар США($) - " + USD_today + f"({USD_difference})\n"
#         elif USD_difference > 0:
#             answer += "Доллар США($) - " + USD_today + f"(+{USD_difference})\n"
#
#         if USD_difference == 0:
#             answer += "Евро(€) - " + EUR_today + "\n"
#         elif USD_difference < 0:
#             answer += "Евро(€) - " + EUR_today + f"({EUR_difference})\n"
#         elif USD_difference > 0:
#             answer += "Евро(€) - " + EUR_today + f"(+{EUR_difference})\n"
#     except:
#         answer = "Не могу получить курс валют:("
#
#     debug_message_to_me(message, answer)
#
#     bot.send_message(message.chat.id,
#                      answer,
#                      reply_markup=KEYBOARD)


# Handle greeting messages
# @bot.message_handler(regexp='^(привет|салют|здравствуй|бонжур|хаюшки|хай|hello|hi|Здорово)')
# def start_messages(message):
#     hello_message = ["Салют!", "Привет!", "здрасти-мордасти.", "о, какие люди!", "физкульт-привет!", "бонжур!",
#                      "приветик!", "здравствуй!", "приветствую!",
#                      "Привет — это такая штука, что если его потеряешь, лучше уже не искать.",
#                      "Ой, здрасте, здрасте, не ожидали!",
#                      "Я что, здоровался с тобой?",
#                      ]
#     answer = f"{random.choice(hello_message).capitalize()}"
#
#     debug_message_to_me(message, answer)
#
#     bot.send_message(message.chat.id,
#                      answer,)


# # Handle good morning messages
# @bot.message_handler(regexp='^(Доброе утро)')
# def start_messages(message):
#     hello_message = ["Доброе утро!",
#                      "Доброе утро начинается с обеда.",
#                      "каждое утро доброе, и оно не виновато, что ты не выспался.",
#                      ]
#     answer = f"{random.choice(hello_message).capitalize()}"
#
#     debug_message_to_me(message, answer)
#
#     bot.send_message(message.chat.id,
#                      answer,)


# # Handle good night  messages
# @bot.message_handler(regexp='^(Спокойной ночи)')
# def start_messages(message):
#     hello_message = ["Спокойной ночи!",
#                      "«Меня ждут в другом месте» — это гораздо лучше, чем «спокойной ночи».",
#                      "Спокойной ночи! Пускай тебе приснится хороший сон обо мне, ладно?",
#                      ]
#     answer = f"{random.choice(hello_message).capitalize()}"
#
#     debug_message_to_me(message, answer)
#
#     bot.send_message(message.chat.id,
#                      answer,)


# Handle name messages
# @bot.message_handler(regexp='тебя зовут|твое имя|своё имя')
# def my_name_messages(message):
#     answer_name_words = ['Меня зовут Бот', 'Я есть Бот!', 'Люди часто называют меня Бот. И ты так зови!', 'Я Бот, просто Бот.',
#                          f'Меня зовут {message.from_user.first_name}. Шучу. Меня зовут Бот.', ]
#     answer = random.choice(answer_name_words)
#
#     debug_message_to_me(message, answer)
#
#     bot.send_message(message.chat.id,
#                      answer,)


# Handle thanks messages
# @bot.message_handler(regexp='спасибо|благодарю|мерси|благодарствую|спасибочки|спс|сяп')
# def thanks_messages(message):
#     answer_thanks_words = ['Рад стараться!',
#                            'Не за что!',
#                            '☺️',
#                            'Обращайся еще!',
#                            'Не стоит благодарности!',
#                            'Из спасибо — шинели не сошьёшь!',
#                            ]
#     answer = random.choice(answer_thanks_words)
#
#     debug_message_to_me(message, answer)
#
#     bot.send_message(message.chat.id,
#                      answer,)


# Handle bot messages
# @bot.message_handler(regexp='^(bot|бот)$')
# def bot_messages(message):
#     answer_bot_words = ['Чего изволите?', 'Что?', 'м?️', 'Что расскажешь?)',
#                         'Я занят, но ради тебя готов освободиться.', ]
#     answer = random.choice(answer_bot_words)
#
#     debug_message_to_me(message, answer)
#
#     bot.send_message(message.chat.id,
#                      answer,)
#
#
# # Handle not wants word messages
# @bot.message_handler(regexp='не хочу|не хотелось|не хотеть|не жаждать|не хотим|не хотела|не хотели')
# def wants_word_messages(message):
#     answer_want_words = ['"Я просила мороженое? Не хочу мороженое, хочу апельсинку."',
#                          'Я тоже много чего не хочу.',
#                          'Не хочу учиться, хочу жениться!',
#                          'Хочу, не хочу - а надо!',
#                          ]
#     answer = random.choice(answer_want_words)
#
#     debug_message_to_me(message, answer)
#
#     bot.send_message(message.chat.id,
#                      answer,)


# Handle wants word messages
# @bot.message_handler(regexp='хочу|хотелось|хотеть|жаждать|хотим|хотела|хотели')
# def wants_word_messages(message):
#     answer_want_words = ['Я тоже много чего хочу.',
#                          'Тебе это не надо.',
#                          'Так сходи и получи это.',
#                          'Я хочу...\nЧего же я хочу?\nКажется, я хочу быть свободным...',
#                          ]
#     answer = random.choice(answer_want_words)
#
#     debug_message_to_me(message, answer)
#
#     bot.send_message(message.chat.id,
#                      answer,)


# ---------------------------------------------
# /schedule                                   -
# Расписание занятий, только одной группы     -
# ---------------------------------------------
# @bot.message_handler(regexp='расписание|пары|занятия|/schedule')
# def schedule_messages(message):
#     schedule = Schedule()
#     answer = schedule.get_lessons(message.text)
#     debug_message_to_me(message, answer)
#     bot.send_message(message.chat.id,
#                      answer,
#                      reply_markup=KEYBOARD)


# ---------------------------------------------
# /newfilms                                   -
# Rutracker парсер новых фильмов              -
# ---------------------------------------------
# @bot.message_handler(regexp='📺Новые фильмы|/newfilms')
# def rutracker_messages(message):
#     answer = ''
#     for item in Rutracker.conclusion(12):
#         answer += f"🎥{item[1]}\n🔗 `{item[0]}` \n 🎙{item[2]} \n ⚖️{item[3]} \n 💎{item[4]}\n-\n"
#     answer = answer[:-2]
#     debug_message_to_me(message, answer)
#     bot.send_message(message.chat.id,
#                      answer,
#                      parse_mode="markdown",
#                      reply_markup=KEYBOARD)


# Handle smile messages
# @bot.message_handler(regexp='хаха|\)\)')
# def smile_messages(message):
#     answer_smile_words = ['Мне нравится когда люди смеются.',
#                           '😊️',
#                           'Мне тоже весело.',
#                           'В дом, где смеются, приходит счастье.',
#                           ]
#     answer = random.choice(answer_smile_words)
#
#     debug_message_to_me(message, answer)
#
#     bot.send_message(message.chat.id,
#                      answer,)


# Handle why messages
# @bot.message_handler(regexp='почему|why')
# def why_messages(message):
#     answer_why_words = ['Я не знаю.',
#                         'Спроси что-то полегче.️',
#                         'Не в моих силах знать:(',
#                         'Откажитесь от «почему» и ищите «как».',
#                         'Иногда на вопрос «почему» нет ответа. И это страшно.',
#                         'Никогда не задаваться вопросом «почему» — главный секрет душевного спокойствия.',
#                         ]
#     answer = random.choice(answer_why_words)
#
#     debug_message_to_me(message, answer)
#
#     bot.send_message(message.chat.id,
#                      answer,)


# ---------------------------------------------
# /story                                      -
# Функция отвечает за истории с баша          -
# ---------------------------------------------
# @bot.message_handler(regexp='скучно|/story|расскажи историю|Случайная история|история')
# def get_story_messages(message):
#     try:
#         target_url = "http://bash.im/random"
#         request = requests.get(target_url)
#         # request.encoding = 'utf-8'
#         soup = BeautifulSoup(request.text, "html.parser")
#         top_titles = soup.find_all("div", {"class": "text"})
#         answer = random.choice(top_titles).text
#     except:
#         answer = "Сегодня нет историй:("
#     debug_message_to_me(message, answer)
#     bot.send_message(message.chat.id,
#                      answer,
#                      reply_markup=KEYBOARD)


# Handle timer messages
# @bot.message_handler(regexp='⏱Таймер')
# def get_story_messages(message):
#     end_time = datetime.datetime(2018, 7, 31, 18, 50)
#     start_time = datetime.datetime.now()
#     difference_time = end_time - start_time
#     answer = f'⏱⏱⏱\nДо отлета самолета(31.07.18 18:50) в Таиланд осталось: \n{difference_time.days}д. {difference_time.seconds//3600}ч. {(difference_time.seconds//60)%60}м. {difference_time.seconds % 60}c.\n⏱⏱⏱'
#     debug_message_to_me(message, answer)
#     bot.send_message(message.chat.id,
#                      answer,
#                      reply_markup=keyboard)


# Handle all other messages
# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_message(message):
#     answer = communication(message)
#     debug_message_to_me(message, answer)
#     bot.send_message(message.chat.id, answer, reply_markup=KEYBOARD)




#
# def communication(message):
#     random.seed()
#
#     colour_words = ["военно-воздушный синий", "синий элис", "ализариновый красный", "миндаль крайола", "амарантовый",
#                "янтарный", "американская роза", "аметистовый", "матовый белый", "античный белый", "яблочно-зелёный",
#                "спаржа",
#                "цвет морской волны", "аквамариновый", "армейский зелёный", "мышьяковый", "лазурный", "голубовато-серый",
#                "бежевый", "чёрный", "синий", "коричневый", "хаки", "медный", "голубой", "изумрудный", "золотой",
#                "зелёный", "оранжевый", "розовый", "фиолетовый", "красный", "серебряный", "томатный", "белый", "жёлтый"]
#     if 'цвет' in message.text.lower():
#         return f"Мне нравится {random.choice(colour_words)}."
#
#
#     choice_words = ['выбрать', 'выбери', "/choice", ]
#     answer_choice_words = ['пусть будет', 'я выбираю', "может быть",
#                            "вышел месяц из тумана, вынул ножик из кармана. буду резать, буду бить – все равно тебе водить! -", ]
#     if any(word in choice_words for word in message.text.lower().split(" ")) and len(
#             [int(s) for s in message.text.split() if s.isdigit()]) > 1:
#         return random.choice(answer_choice_words) + " " + str(
#                 random.choice([int(s) for s in message.text.split() if s.isdigit()]))
#
#     my_message = ["Так себе", "Давай что-то другое", "Великолепно", "Быть может", "Заманчивая идея!", "Может не стоит",
#                   "Чудесно!", "предлагаю сегодня поучиться", "мне приятно с тобой общаться",
#                   "Я тебя не понимаю", "давай потом об этом поговорим", ]
#     return random.choice(my_message)






