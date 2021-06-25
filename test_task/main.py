import aioredis
import asyncpg
from fastapi import FastAPI, Response, status

from functions import get_devices, get_check
from schemas import Anagram

app = FastAPI()


@app.post('/anagram/')
async def anagram(item: Anagram):
    '''
    https://webdevblog.ru/redis-dlya-nachinajushhij/ to do review cod
    :param item:
    :return:
    '''
    flag = get_check(item)
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


@app.get('/create-tables/')
async def create_table_device():
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    await conn.execute("CREATE TABLE device(id serial PRIMARY KEY, dev_id varchar , dev_type varchar)")
    await conn.execute(
        "CREATE TABLE endpoint(id serial PRIMARY KEY, device_id INT, FOREIGN KEY (device_id) REFERENCES device (id) ON DELETE CASCADE)")
    await conn.close()
    return {'status': 'OK'}


@app.get('/devices-into-db/', status_code=200)
async def device_into(response: Response):
    count_el = 10
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    devices = get_devices(count_el)
    for el in devices:
        await conn.execute('''
                            INSERT INTO device(dev_id, dev_type) VALUES($1, $2)
                            ''',
                           el['dev_id'], el['dev_type'])
    device_id = await conn.fetch('SELECT id FROM device ORDER BY RANDOM() LIMIT 5')
    for el in device_id:
        await conn.execute('''
                            INSERT INTO endpoint(device_id) VALUES($1)
                            ''',
                           el['id'])
    await conn.close()
    response.status_code = status.HTTP_201_CREATED
    return {'status': '201'}


@app.get('/get_all_device_without_endpoint/')
async def get_all_device_without_endpoint():
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    all_devices = await conn.fetch(
        'SELECT * FROM device WHERE id NOT IN (SELECT device_id FROM endpoint) ORDER BY dev_type')
    await conn.close()
    return all_devices


@app.get('/devices-from-db/')
async def get_all_devices_from_db():
    """
     function for control
    :return:
    """
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    rows = await conn.fetch('SELECT * FROM device')
    await conn.close()
    return rows


@app.get('/get_all_endpoint/')
async def get_all_endpoint():
    """
    function for control
    :return:
    """
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    all_endpoint = await conn.fetch('SELECT * FROM endpoint')
    await conn.close()
    return all_endpoint


@app.delete('/drop-table-device')
async def delete_table_device():
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    await conn.execute("DROP TABLE device")
    await conn.close()
    return {'status': 'OK'}


@app.delete('/drop-table-endpoint')
async def delete_table_endpoint():
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:8010/stage')
    await conn.execute("DROP TABLE endpoint")
    await conn.close()
    return {'status': 'OK'}
