import requests


def get_friends_list(user_id, access_token):
        res = requests.get(f'https://api.vk.com/method/friends.get',
                                params={
                                   'access_token': access_token,
                                   'count': '5',
                                   'order': 'random',
                                   'user_id': user_id,
                                   'v': '5.120',
                                })
        data = res.json()
        friends_list = data['response']["items"]
        return tuple(friends_list)


def get_profile(user_id, access_token):
    res = requests.get(f'https://api.vk.com/method/users.get',
                                params={
                                   'access_token': access_token,
                                   'v': '5.120',
                                   'user_id': str(user_id),
                                   'fields': "uid,first_name,photo_400_orig"
                                })
    data = res.json()
    return data['response'][0]


def get_user_id(access_token):
    res = requests.get(f'https://api.vk.com/method/getProfiles',
                    params={
                       'access_token': access_token,
                       'v': '5.120',
                    })
    data = res.json()
    user_id = data['response'][0]['id']
    return str(user_id)