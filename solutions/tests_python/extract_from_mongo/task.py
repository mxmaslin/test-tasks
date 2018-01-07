# -*- coding: utf-8 -*-
from mongoengine import *
import enum
import random
import unittest

from pprint import pprint

class ImagesEnum(enum.Enum):
    cover = 'cover'
    background = 'background'
    foreground = 'foreground'


class QualityEnum(enum.IntEnum):
    LD = 0
    SD = 1
    HD = 2
    FULL_HD = 3


class File(EmbeddedDocument):
    path = StringField()
    quality = IntField()


class Quote(EmbeddedDocument):
    source = StringField()
    text = StringField()


class Episode(EmbeddedDocument):
    num = IntField()
    alias = StringField()
    files = EmbeddedDocumentListField('File')


class Season(Document):
    num = IntField()
    alias = StringField()
    episodes = EmbeddedDocumentListField('Episode', db_field='items')
    meta = {
        'collection': 'products',
        'allow_inheritance': True
    }


class Series(Document):
    title = StringField()
    alias = StringField()
    description = StringField()
    seasons = ListField(ReferenceField('Season'), db_field='items')
    quote = EmbeddedDocumentField('Quote')
    images = MapField(URLField())
    meta = {
        'collection': 'products',
        'allow_inheritance': True
    }


class TestTask(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connect('test', host='mongo')

    def test_01_create_documents(self):
        def __quote(i):
            source = 'QuoteSource %i' % i
            return {'source': source, 'text': 'test quote'}

        def __images(i):
            return {img.value: 'image path %i' % i for img in ImagesEnum}

        def __files():
            files = list()
            for i in QualityEnum:
                f = File(quality=i, path='file path %i' % i)
                files.append(f)
            return files

        def __episodes():
            episodes = list()
            for i in range(0, random.randint(1, 30)):
                s = Episode(num=i, alias='episode%i' % i, files=__files())
                episodes.append(s)
            return episodes

        def __seasons():
            seasons = list()
            for i in range(0, random.randint(1, 10)):
                s = Season(num=i, alias='season%i' % i, episodes=__episodes())
                s.save()
                seasons.append(s)
            return seasons

        def __series():
            series = list()
            for i in range(0, random.randint(1, 10)):
                s = Series.objects(
                    title='series %i' % i,
                    alias='series%i' % i
                    ).modify(
                        upsert=True,
                        new=True,
                        set__quote=__quote(i),
                        set__images=__images(i),
                        set__description='description %i' % i,
                        set__seasons=__seasons())
                series.append(s)
            return series
        self.assertTrue(__series())

    def test_02_create_documents(self):
        """
            Напишите запрос который вернет ответ следующего формата:
            [
              {
                "path": "/series/<alias сериала>",
                "title": "<title сериала>",
                "description": "<description сериала>",
                "cover": "<изображение из поля images с ключем ImagesEnum.cover>",
                "quote": "<значение quote.text>",
                "quote_source": "<значение quote.source>",
                "slide": {
                  "background": "<изображение из поля images с ключем ImagesEnum.background>",
                  "foreground": "<изображение из поля images с ключем ImagesEnum.foreground>"
                }
                "seasons": [
                  {
                    "path": "/series/<alias сериала>/<alias сезона>",
                    "title": "<num сезона> сезон",
                    "episodes": [
                      {
                        "path": "/series/<alias сериала>/<alias сезона>/<alias эпизода>",
                        "title": "Эпизод <num сезона>",
                        "files": [
                          {
                            "path": "<path файла>",
                            "label": "<название enum поля QualityEnum>",
                            "quality": "<значения enum поля QualityEnum>"
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
        """
        result = []
        for serie in Series.objects:
            serie_dict = dict()
            serie_dict['path'] = "/series/" + serie.alias
            serie_dict['title'] = serie.title
            serie_dict['description'] = serie.description
            serie_dict['cover'] = serie.images[ImagesEnum.cover.name]
            serie_dict['quote'] = serie.quote.text
            serie_dict['quote_source'] = serie.quote.source
            serie_dict['slide'] = {
                'background': serie.images[ImagesEnum.background.name],
                'foreground': serie.images[ImagesEnum.foreground.name]
            }
            serie_dict['seasons'] = []
            for season in serie.seasons:
                season_dict = dict()
                season_dict['path'] = '{}/{}'.format(serie_dict['path'], season.alias)
                season_dict['title'] = season.num
                season_dict['episodes'] = []
                for episode in season.episodes:
                    episode_dict = dict()
                    episode_dict['path'] = '{}/{}'.format(season_dict['path'], episode.alias)
                    episode_dict['title'] = 'Эпизод {}'.format(episode.num)
                    episode_dict['files'] = []
                    for file in episode.files:
                        file_dict = dict()
                        file_dict['path'] = file.path
                        file_dict['quality'] = file.quality
                        file_dict['label'] = QualityEnum(file.quality).name
                        episode_dict['files'].append(file_dict)
                    season_dict['episodes'].append(episode_dict)
                serie_dict['seasons'].append(season_dict)


            result.append(serie_dict)
        return result

if __name__ == '__main__':
    unittest.main()
