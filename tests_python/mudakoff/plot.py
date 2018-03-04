# -*- coding: utf-8 -*-
from bokeh.plotting import figure, output_file, show
from functools import reduce
import time, datetime
import vk_api


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
    login, password = 'mfilimonova2007@yandex.ru', 'MamAni'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    return vk_session.get_api()

def main():
    vk = set_vk_session()
    likes_prev, comments_prev, reposts_prev = count_posts_portion(vk)
    first_iteration = True

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

            output_file('bokeh_test.html')
            p = figure(
            title='bokeh test',
            x_axis_label='x',
            y_axis_label='y')
            datetime.now()
            p.line(x=datetime.now(),
                   y=likes_change,
                   legend='bokeh test',
                   line_width=2)






if __name__ == '__main__':
    main()
