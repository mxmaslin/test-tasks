# -*- coding: utf-8 -*-
import time
import vk_api


def count_stuff(vk):
    posts_amount = vk.wall.get(domain='mudakoff', count=1)['count']
    offset_counter = 0
    countdown_start_time = time.ctime()
    likes = 0
    comments = 0
    reposts = 0
    while offset_counter < posts_amount:
        if posts_amount - offset_counter < 100:
            offset_counter += posts_amount - offset_counter
        else:
            offset_counter += 100
        for post in vk.wall.get(domain='mudakoff', count=1, offset=offset_counter)['items']:
            likes += post['likes']['count']
            comments += post['comments']['count']
            reposts += post['reposts']['count']
    return {'time': countdown_start_time, 'values': [likes, comments, reposts]}


def main():
    login, password = 'mxmaslin@gmail.com', 'q1w2e3r4'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    likes_prev, comments_prev, reposts_prev = count_stuff(vk)['values']
    first_iteration = True

    while True:
        if first_iteration:
            likes_now, comments_now, reposts_now = likes_prev, comments_prev, reposts_prev
            first_iteration = False
            continue
        likes_prev, comments_prev, reposts_prev = likes_now, comments_now, reposts_now
        likes_now, comments_now, reposts_now = count_stuff(vk)['values']
        likes_change = ((likes_now - likes_prev) / likes_prev) * 100
        comments_change = ((comments_now - comments_prev) / comments_prev) * 100
        reposts_change = ((reposts_now - reposts_prev) / reposts_prev) * 100

        print(likes_change, comments_change, reposts_change)
        print('-')


if __name__ == '__main__':
    main()
