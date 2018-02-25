# -*- coding: utf-8 -*-
import time, datetime
import plotly
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
import vk_api

plotly.tools.set_credentials_file(username='mxmaslin', api_key='SxjPplGYZgYgbi69kwrc')


def count_posts_portion(vk):
    posts_amount = vk.wall.get(domain='mudakoff')['count']
    offset_counter = 0
    likes = 0
    comments = 0
    reposts = 0
    while offset_counter < posts_amount:
        for post in vk.wall.get(domain='mudakoff', count=100, offset=offset_counter)['items']:
            likes += post['likes']['count']
            comments += post['comments']['count']
            reposts += post['reposts']['count']
        offset_counter += 100
    return likes, comments, reposts


def set_vk_session():
    login, password = 'your_login', 'your_password'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    return vk_session.get_api()


def main():
    stream_ids = tls.get_credentials_file()['stream_ids']

    stream_1 = go.Stream(
        token=stream_ids[0],
        maxpoints=80)
    stream_2 = go.Stream(
        token=stream_ids[1],
        maxpoints=80)
    stream_3 = go.Stream(
        token=stream_ids[2],
        maxpoints=80)

    trace1 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_1,
        name='Лайки')
    trace2 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_2,
        name='Комментарии')
    trace3 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_3,
        name='Репосты')

    data = go.Data([trace1, trace2, trace3])

    layout = go.Layout(title='Изменение количества лайков/комментариев/репостов сообщества http://vk.com/mudakoff')
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='python-streaming')

    s1 = py.Stream(stream_ids[0])
    s1.open()
    s2 = py.Stream(stream_ids[1])
    s2.open()
    s3 = py.Stream(stream_ids[2])
    s3.open()

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

            x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            s1.write(dict(x=x, y=likes_change))
            s2.write(dict(x=x, y=comments_change))
            s3.write(dict(x=x, y=reposts_change))

            print(x)
            print(likes_change, likes_now, likes_prev)
            print(comments_change, comments_now, comments_prev)
            print(reposts_change, reposts_now, reposts_prev)
            print('')

            time.sleep(1)

    s1.close()
    s2.close()
    s3.close()
    tls.embed('streaming-demos', '12')


if __name__ == '__main__':
    main()
