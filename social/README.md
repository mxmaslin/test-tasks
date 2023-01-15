# Разогревы

## Разогрев 1

Распишите пример(ы) unit тестов на эту фyнкцию:

```
async def logs(cont, name):
    conn = aiohttp.UnixConnector(path='/var/run/docker.sock')
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(f'http://xx/containers/{cont}/logs?follow=1&stdout=1') as resp:
            async for line in resp.content:
                print(name, line)
```

**Результат**

```
import aiohttp
import pytest

@pytest.mark.asyncio
async def test_logs(aioresponses, capsys):
    cont = '1234'
    name = 'container_name'
    aioresponses.get(f'http://xx/containers/{cont}/logs?follow=1&stdout=1', status=200, body='test log')
    await logs(cont, name)
    captured = capsys.readouterr()
    assert captured.out == "container_name b'test log'\n"
```

## Разогрев 2

Напишите эндпойнт, который в качестве параметра сможет принимать незакодированную (unencoded) ссылку и возвращать её закодированной.

**Результат**

```
from flask import Flask, request, jsonify
import urllib.parse

app = Flask(__name__)

@app.route('/encode', methods=['GET'])
def encode():
    unencoded_url = request.args.get('url')
    data = {'encoded_url': None}
    try:
        encoded_url = urllib.parse.quote(unencoded_url)
    except:
        return jsonify(data), 500
    data['endoded_url'] = encoded_url
    return jsonify(data), 200

if __name__ == '__main__':
    app.run()
```

# Основное задание

Create a simple RESTful API using FastAPI for a social networking application

## Functional requirements

There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..)

- As a user I need to be able to signup and login
- As a user I need to be able to create, edit, delete and view posts
- As a user I can like or dislike other users’ posts but not my own 
- The API needs a UI Documentation (Swagger/ReDoc)

Bonus section (not required):

- Use https://clearbit.com/platform/enrichment for getting additional data for the user on signup
- Use emailhunter.co for verifying email existence on registration
- Use an in-memory DB for storing post likes and dislikes (As a cache, that gets updated whenever new likes and dislikes get added) 

## Technology Requirements

Tasks should be completed:

- Using FastAPI 0.50.0+
- With any DBMS (Sqlite, PostgreSQL, MySQL)
- Uploaded to GitHub

## Requirements

When implementing your solution, please make sure that the code is:

- Well-structured
- Contains instructions (best to be put into readme.md) about how to deploy and test it
- Clean
- The program you implement must be a complete program product, i.e. should be easy to install, provide for the handling of non-standard situations, be resistant to incorrect user actions, etc.
