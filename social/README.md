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

