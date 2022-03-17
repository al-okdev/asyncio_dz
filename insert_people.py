import asyncio
# import random
import time

import aiohttp
import asyncpg
import more_itertools
from more_itertools import chunked
# from faker import Faker

import config

# fake = Faker()

url = 'https://swapi.dev/api'

async def get_person(person_id):
    print(person_id)
    session = aiohttp.ClientSession()
    response = await session.get(f'{url}/people/{person_id}')
    response_json = await response.json()
    await session.close()
    if 'name' in response_json:
        print(response_json['name'])
        return [(response_json['birth_year'], response_json['eye_color'], " ".join(response_json['films']),
                  response_json['gender'], response_json['hair_color'], response_json['height'], response_json['homeworld'],
                  response_json['mass'], response_json['name'], response_json['skin_color'], " ".join(response_json['species']),
                  " ".join(response_json['starships']), " ".join(response_json['vehicles']))]
    else:
        return [('-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-')]



async def get_people(people_ids):
    tasks = [asyncio.create_task(get_person(person_id)) for person_id in people_ids]
    for task in tasks:
        tasks_result = await task
        yield tasks_result

async def insert_users(pool: asyncpg.Pool, user_list):
    query = 'INSERT INTO users (birth_year, eye_color, films, gender, hair_color, height, homeworld, mass, name, ' \
            'skin_color, species, starships, vehicles) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)'
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(query, user_list)


async def main():
    pool = await asyncpg.create_pool(config.PG_DSN, min_size=20, max_size=20)

    for person_ids_chunk in more_itertools.chunked(range(1, 100), 10):
        tasks = []
        async for person in get_people(person_ids_chunk):
            tasks.append(asyncio.create_task(insert_users(pool, person)))

    await asyncio.gather(*tasks)
    await pool.close()

start = time.time()
asyncio.run(main())
print('Время работы ', time.time() - start)