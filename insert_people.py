import asyncio
# import random

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
    print(response_json['name'])
    yield (
        response_json['name'],
        response_json['gender']
    )
    await session.close()

# def gen_users_data(quantity: int):
#
#     for _ in range(quantity):
#         yield (
#             fake.name(),
#             random.choice(['a', 'b', 'c', 'd'])
#         )


async def insert_users(pool: asyncpg.Pool, user_list):
    query = 'INSERT INTO users (name, gender) VALUES ($1, $2)'
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(query, user_list)


async def main():
    pool = await asyncpg.create_pool(config.PG_DSN, min_size=20, max_size=20)

    # for users_chunk in chunked(gen_users_data(20), 10):
    #     tasks.append(asyncio.create_task(insert_users(pool, users_chunk)))

    ###
    for person_ids_chunk in more_itertools.chunked(range(1, 20), 10):
        tasks = []
        for person_id in person_ids_chunk:
            tasks.append(asyncio.create_task(insert_users(pool, [('44', '55')] )))
        # task_results = await asyncio.gather(*list_of_task)
    ###


    await asyncio.gather(*tasks)
    await pool.close()

if __name__ == '__main__':
    asyncio.run(main())