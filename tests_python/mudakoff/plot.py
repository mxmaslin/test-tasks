# -*- coding: utf-8 -*-
import vk_api
from datetime import datetime
from functools import reduce

from bokeh.plotting import figure, output_file, show


def count_posts_portion(vk):
    posts_amount = vk.wall.get(domain='mudakoff')['count']
    offset_counter = 0
    likes = 0
    comments = 0
    reposts = 0
    while offset_counter < posts_amount:
        posts = vk.wall.get(domain='mudakoff', count=100, offset=offset_counter)['items']
        likes += reduce(lambda a, post: a + post['likes']['count'], posts, 0)
        comments += reduce(lambda a, post: a + post['comments']['count'], posts, 0)
        reposts += reduce(lambda a, post: a + post['reposts']['count'], posts, 0)
        offset_counter += 100
    return likes, comments, reposts


def set_vk_session():
    login, password = 'login', 'password'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        exit()
    return vk_session.get_api()


def main():
    vk = set_vk_session()
    likes_prev, comments_prev, reposts_prev = count_posts_portion(vk)
    first_iteration = True

    output_file('plot.html')
    x = [datetime.now()]
    y_likes_change = [0]
    y_comments_change = [0]
    y_reposts_change = [0]
    p = figure(
        title='Динамика лайков, комментариев, репостов в mudakoff',
        x_axis_label='Время',
        y_axis_label='Количество')
    p.line(x, y_likes_change, legend='Лайки', line_width=2, line_color='red')
    p.line(x, y_comments_change, legend='Комментарии', line_width=2, line_color='green')
    p.line(x, y_reposts_change, legend='Репосты', line_width=2, line_color='blue')
    show(p)

    while True:
        if first_iteration:
            likes_now, comments_now, reposts_now = likes_prev, comments_prev, reposts_prev
            first_iteration = False
            continue
        else:
            likes_prev, comments_prev, reposts_prev = likes_now, comments_now, reposts_now
            likes_now, comments_now, reposts_now = count_posts_portion(vk)

            likes_change = likes_now - likes_prev
            comments_change = comments_now - comments_prev
            reposts_change = reposts_now - reposts_prev

            x.append(datetime.now())
            y_likes_change.append(likes_change)
            y_comments_change.append(comments_change)
            y_reposts_change.append(reposts_change)
            p.line(x, y_likes_change, legend='Лайки', line_width=2, line_color='red')
            p.line(x, y_comments_change, legend='Комментарии', line_width=2, line_color='green')
            p.line(x, y_reposts_change, legend='Репосты', line_width=2, line_color='blue')
            show(p)


if __name__ == '__main__':
    main()
