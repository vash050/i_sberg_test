import aioredis
import asyncpg
from fastapi import FastAPI, Response, status

from functions import get_devices, get_check
from schemas import Anagram

app = FastAPI()


@app.post('/anagram/')
async def anagram(item: Anagram):
    """
    the function takes two strings, checks whether they are anagrams, and returns the number of positive checks and the
    result of this check
    :param item: object model Anagram
    :return: dict
    """
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
    redis.close()
    await redis.wait_closed()

    return {'key': flag, 'count': count}


@app.get('/create-tables/')
async def create_table_device():
    async with asyncpg.create_pool(dsn='postgresql://postgres:postgres@localhost:8010/stage',
                                   command_timeout=60) as pool:
        async with pool.acquire() as conn:
            await conn.execute(
                "CREATE TABLE device(id serial PRIMARY KEY, dev_id varchar(200) NOT NULL, dev_type varchar(120) NOT NULL)")
            await conn.execute(
                "CREATE TABLE endpoint(id serial PRIMARY KEY, device_id INT, FOREIGN KEY (device_id) REFERENCES device (id) ON DELETE CASCADE)")
            await conn.close()
    return {'status': 'OK'}


@app.get('/devices-into-db/', status_code=200)
async def device_into(response: Response):
    count_el = 10
    async with asyncpg.create_pool(dsn='postgresql://postgres:postgres@localhost:8010/stage',
                                   command_timeout=60) as pool:
        async with pool.acquire() as conn:
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
    return {'status': 'OK'}


@app.get('/get_all_device_without_endpoint/')
async def get_all_device_without_endpoint():
    async with asyncpg.create_pool(dsn='postgresql://postgres:postgres@localhost:8010/stage',
                                   command_timeout=60) as pool:
        async with pool.acquire() as conn:
            all_devices = await conn.fetch(
                'SELECT dev_type, count(dev_type) FROM device WHERE id NOT IN (SELECT device_id FROM endpoint) GROUP BY dev_type')
            await conn.close()
    return all_devices


@app.get('/devices-from-db/')
async def get_all_devices_from_db():
    """
     function for control
    :return:
    """
    async with asyncpg.create_pool(dsn='postgresql://postgres:postgres@localhost:8010/stage',
                                   command_timeout=60) as pool:
        async with pool.acquire() as conn:
            rows = await conn.fetch('SELECT * FROM device')
            await conn.close()
    return rows


@app.get('/get_all_endpoint/')
async def get_all_endpoint():
    """
    function for control
    :return:
    """
    async with asyncpg.create_pool(dsn='postgresql://postgres:postgres@localhost:8010/stage',
                                   command_timeout=60) as pool:
        async with pool.acquire() as conn:
            all_endpoint = await conn.fetch('SELECT * FROM endpoint')
            await conn.close()
    return all_endpoint


@app.delete('/drop-table-device')
async def delete_table_device():
    async with asyncpg.create_pool(dsn='postgresql://postgres:postgres@localhost:8010/stage',
                                   command_timeout=60) as pool:
        async with pool.acquire() as conn:
            await conn.execute("DROP TABLE device")
            await conn.close()
    return {'status': 'OK'}


@app.delete('/drop-table-endpoint')
async def delete_table_endpoint():
    async with asyncpg.create_pool(dsn='postgresql://postgres:postgres@localhost:8010/stage',
                                   command_timeout=60) as pool:
        async with pool.acquire() as conn:
            await conn.execute("DROP TABLE endpoint")
            await conn.close()
    return {'status': 'OK'}
