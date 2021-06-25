from fastapi import FastAPI

import asyncio
import aioredis
import asyncpg

from functions import get_devices
from schemas import Anagram

app = FastAPI()


@app.get('/')
def home():
    return {"key": "Hello"}


@app.post('/anagram/')
async def anagram(item: Anagram):
    '''
    https://webdevblog.ru/redis-dlya-nachinajushhij/ to do review cod
    :param item:
    :return:
    '''
    new_str_1 = [x for x in item.str_1 if x.isalpha() or x.isdigit()]
    new_str_2 = [x for x in item.str_2 if x.isalpha() or x.isdigit()]

    str_1_pars = "".join(new_str_1).lower()
    str_2_pars = "".join(new_str_2).lower()

    flag = False
    if len(str_1_pars) == len(str_2_pars):
        for el in str_1_pars:
            flag = el in str_2_pars
            if flag is False:
                break
    redis = await aioredis.create_redis_pool('redis://localhost:6379')
    count = await redis.get('count', encoding='utf-8')
    if flag:
        if count:
            count = int(count)
            count += 1
        else:
            count = 1
        await redis.set('count', count)
    redis = await aioredis.create_redis_pool('redis://localhost:6379')
    redis.close()
    await redis.wait_closed()

    return {'key': flag, 'count': count}


@app.get('/drop-table-device')
async def delete_table_device():
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    await conn.execute("DROP TABLE devices")
    await conn.close()
    return {'status': 'OK'}


@app.get('/create-table-devices/')
async def create_table_devices():
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    await conn.execute("CREATE TABLE devices(id serial PRIMARY KEY, dev_id varchar , dev_type varchar)")
    await conn.close()
    return {'status': 'OK'}


@app.get('/create-table-endpoint/')
async def create_table_devices():
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    await conn.execute("CREATE TABLE endpoint(id serial PRIMARY KEY, device_id INT, FOREIGN KEY (device_id) REFERENCES devices (id) ON DELETE CASCADE)")
    await conn.close()
    return {'status': 'OK'}


@app.get('/devices-into-db/')
async def device_into():
    count_el = 10
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    devices = get_devices(count_el)
    for device in devices:
        await conn.execute('''
                            INSERT INTO devices(dev_id, dev_type) VALUES($1, $2)
                            ''',
                           device['dev_id'], device['dev_type'])
    await conn.close()
    return {'status': '201'}


@app.get('/devices-from-db/')
async def get_devices_from_db():
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    rows = await conn.fetch('SELECT * FROM devices')
    await conn.close()
    return rows


@app.get('/devices-from-db-5-random/')
async def get_devices_from_db():
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    rows = await conn.fetch('SELECT * FROM devices ORDER BY RANDOM() LIMIT 5')
    await conn.close()
    return rows
