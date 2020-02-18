# rutracker parser api
# ЗАДАЧИ:
# - Один фильм - один раз упоминается
# - Рейтинг фильмов
import requests


class Rutracker:
    __request_url = 'http://api.rutracker.org/v1/static/pvc/f/' + '1950'  # 1950 - фильмы 2018

    @classmethod
    def get_all_topics(cls):
        response = requests.get(cls.__request_url)
        return response.json()

    @classmethod
    def get_info(cls, id):
        request_url = 'http://api.rutracker.org/v1/get_tor_topic_data?by=topic_id&val=' + id
        response = requests.get(request_url)
        return response.json()

    @classmethod
    def conclusion(cls, limit=40):
        id_topics = list(cls.get_all_topics()['result'].keys())[-limit:]
        limited_dict_of_topics = cls.get_info(','.join(id_topics))['result']
        limited_list_of_topics = []
        for id in id_topics:
            limited_list_of_topics.append([
                                           # id,  # id темы
                                           limited_dict_of_topics[id]['info_hash'],  # hash файла
                                           limited_dict_of_topics[id]['topic_title'][0:limited_dict_of_topics[id]['topic_title'].find('/')].strip(),
                                           # Название фильма
                                           # limited_dict_of_topics[id]['topic_title'][limited_dict_of_topics[id]['topic_title'].find('[') + 1:limited_dict_of_topics[id]['topic_title'].find(']')].strip(),
                                           # краткое описание
                                           limited_dict_of_topics[id]['topic_title'][limited_dict_of_topics[id]['topic_title'].find(']') + 1:].strip(),  # Перевод
                                           round(limited_dict_of_topics[id]['size'] / 1073741824, 2),  # Размер
                                           limited_dict_of_topics[id]['seeders'],  # Количество сидеров
                                           ])

        return limited_list_of_topics


if __name__ == '__main__':
    answer = ''
    # for item in Rutracker.conclusion(5):
    #     answer += item

    print(Rutracker.conclusion())


