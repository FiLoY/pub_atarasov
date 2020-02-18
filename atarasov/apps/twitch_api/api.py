import requests


class TwitchStartPointApi:
    url = 'https://api.twitch.tv/helix/'
    def __init__(self, token=None):
        self.token = 'amqvnce0hsnfm72aad3zb3fq6gc8ln'

    def __getattr__(self, method):
        self.url += method + '/'
        return Backend(self)


class Backend:
    def __init__(self, start_point_api):
        self.start_point_api = start_point_api

    def __call__(self, *args, **kwargs):
        headers = {"Authorization": "Bearer " + self.start_point_api.token}
        if kwargs:
            self.start_point_api.url += '?'
            for k, v in kwargs.items():
                self.start_point_api.url += k + '=' + v + '&'
        data = requests.get(self.start_point_api.url, headers=headers).json()['data']
        self.start_point_api.url = 'https://api.twitch.tv/helix/'
        return data

    def __getattr__(self, method):
        self.start_point_api.url += method + '/'
        return Backend(self.start_point_api)

if __name__ == '__main__':
    helix = TwitchStartPointApi()
    subscriptions = helix.webhooks.subscriptions()

    names = []
    for stream in subscriptions:
        user_id = stream['topic'].split('=')[1]
        names.append(helix.users(id=user_id)[0]['login'])
    print(names)
        # print()
    # print(helix.webhooks.subscriptions())
    # print(helix.streams(user_id=))
