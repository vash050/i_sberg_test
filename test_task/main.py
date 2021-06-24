from fastapi import FastAPI

import asyncio
import aioredis

from schemas import Anagram

app = FastAPI()




# @app.on_event("startup")
# async def startup():
#     # когда приложение запускается устанавливаем соединение с БД
#     redis = await aioredis.create_redis_pool('redis://localhost:6379')
#     await redis.set('my-key', 'value')
#     value = await redis.get('my-key', encoding='utf-8')
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     # когда приложение останавливается разрываем соединение с БД
#     redis = await aioredis.create_redis_pool('redis://localhost:6379')
#     redis.close()
#     await redis.wait_closed()


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
