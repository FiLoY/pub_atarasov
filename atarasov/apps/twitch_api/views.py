from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

import json
import logging
import requests

from apps.telegram_bot.views import bot


# ---------------------------------------------
# Вход бота                                   -
# Основная вьюшка для бота                    -
# ---------------------------------------------
# SUBSCRIBE!!!
# http POST 'https://api.twitch.tv/helix/webhooks/hub' 'Authorization':' Bearer <ACCESS_TOKEN>' hub.callback=https://atarasov.ru/twitch_api/ hub.mode='subscribe' hub.lease_seconds=864000 hub.topic='https://api.twitch.tv/helix/streams?user_id=57800626'

streams = {}

# JUST TEST in Local
# request_str = '{"data":[{"game_id":"509549","id":"360372385","language":"ru","started_at":"2019-12-26T10:55:50Z","tag_ids":["0569b171-2a2b-476e-a596-5bdfb45a1327"],"thumbnail_url":"https://static-cdn.jtvnw.net/previews-ttv/live_user_dreadztv-{width}x{height}.jpg","title":"Dread\'s stream. GG.BET. Стримим с помощью ноутбука Asus ROG Zephyrus S.","type":"live","user_id":"57800626","user_name":"FiLoY1","viewer_count":558},' \
#               '{"game_id":"509549","id":"360372385","language":"ru","started_at":"2019-12-26T10:55:50Z","tag_ids":["0569b171-2a2b-476e-a596-5bdfb45a1327"],"thumbnail_url":"https://static-cdn.jtvnw.net/previews-ttv/live_user_dreadztv-{width}x{height}.jpg","title":"Dread\'s stream. GG.BET. Стримим с помощью ноутбука Asus ROG Zephyrus S.","type":"live","user_id":"7777777","user_name":"FiLoY1","viewer_count":558} ]}'
# data = json.loads(request_str)['data']
# for stream in data:
#     streams[stream['user_id']] = {'game_id': stream['game_id'], 'title': stream['title']}
# # print(streams)
# env = environ.Env()
#
# url = 'https://api.twitch.tv/helix/webhooks/subscriptions'
# headers = {"Authorization": "Bearer " + env('TWITCH_TOKEN')}
# subscriptions = requests.get(url, headers=headers).json()['data']
#
# active_streams = []
# for subscription in subscriptions:
#     topic = requests.get(subscription['topic'], headers=headers).json()['data']
#     try:
#         active_streams += [topic[0]['user_id']]
#     except IndexError:
#         pass
#     # print(topic)
#
# for stream in streams:
#     if stream not in active_streams:
#         del streams[stream]
#         break
# print(streams)


# g = requests.get(subscriptions[0]['topic'], headers=headers).json()['data']
# print(subscriptions)
# logging.basicConfig(filename="sample.log", format='%(asctime)s (%(levelname)s) %(name)s: %(message)s', datefmt='%d/%b/%Y %H:%M:%S')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@csrf_exempt
def bot_view(request):
    log.info('START')
    headers = {"Authorization": "Bearer " + settings.TWITCH_TOKEN}
    log.info(request.META.get('HTTP_X_FORWARDED_FOR'))
    log.info(request)

    if 'CONTENT_TYPE' in request.META and 'application/json' in request.META['CONTENT_TYPE']:
        try:
            log.info(request.body.decode("utf-8"))
            data = json.loads(request.body.decode("utf-8"))['data'][0]
            send_string = 'Ничего не случилось, но что-то произошло...'
            if data['user_id'] in streams:
                if data['game_id'] != streams[data['user_id']]['game_id']:
                    url = 'https://api.twitch.tv/helix/games?id=' + data['game_id']
                    game_name = requests.get(url, headers=headers).json()['data'][0]['name']
                    send_string = f"<b>Стример</b> <code>{data['user_name']}</code> <b>сменил игру!</b>\n" \
                                  f"Теперь это - <code>{game_name}</code>\n" \
                                  f"Количество зрителей: <code>{data['viewer_count']}</code>"
                    log.info(send_string)

                elif data['title'] != streams[data['user_id']]['title']:
                    send_string = f"<b>Стример</b> <code>{data['user_name']}</code> <b>сменил название трансляции на:</b>\n" \
                                  f"<code>{data['title']}</code>\n" \
                                  f"Количество зрителей: <code>{data['viewer_count']}</code>"
                    log.info(send_string)
            else:
                url = 'https://api.twitch.tv/helix/games?id=' + data['game_id']
                game_name = requests.get(url, headers=headers).json()['data'][0]['name']
                send_string = f"<b>Стример</b> <code>{data['user_name']}</code> <b>запустил трансляцию!</b>\n" \
                              f"Название: <code>{data['title']}</code>\n" \
                              f"Игра: <code>{game_name}</code>\n" \
                              f"Ссылка: https://twitch.tv/{data['user_name']}/\n"
                log.info(send_string)

            bot.send_message(chat_id=180469947, text=send_string, parse_mode="html")
            log.info('END')


            streams[data['user_id']] = {'user_name': data['user_name'], 'game_id': data['game_id'], 'title': data['title']}
        except IndexError as e:
            log.error(e)
            # Delete not active stream
            url = 'https://api.twitch.tv/helix/webhooks/subscriptions'
            subscriptions = requests.get(url, headers=headers).json()['data']

            active_streams = []
            for subscription in subscriptions:
                topic = requests.get(subscription['topic'], headers=headers).json()['data']
                try:
                    active_streams += [topic[0]['user_id']]
                except IndexError as e:
                    log.error(e)

            for key in streams:
                if key not in active_streams:
                    send_string = f"Стример <code>{streams[key]['user_name']}</code> закончил трансляцию!\n"
                    bot.send_message(chat_id=180469947, text=send_string, parse_mode="html")
                    del streams[key]
                    log.info('END')
                    break
        except Exception as e:
            log.error(e)
        return HttpResponse(status=200)
    else:
        log.error('CONTENT_TYPE is not JSON')
        try:
            return HttpResponse(request.GET['hub.challenge'], status=200)
        except Exception as e:
            log.error(e)
        return redirect('home')










