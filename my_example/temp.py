import asyncio
import random

import asyncpg
from more_itertools import chunked
from faker import Faker

import config

fake = Faker()


def gen_users_data(quantity: int):

    for _ in range(quantity):
        yield (
            fake.name(),
            random.choice(['a', 'b', 'c', 'd'])
        )


async def insert_users(pool: asyncpg.Pool, user_list):
    print(user_list)
    query = 'INSERT INTO users (name, gender) VALUES ($1, $2)'
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(query, user_list)


async def main():
    pool = await asyncpg.create_pool(config.PG_DSN, min_size=20, max_size=20)
    tasks = []
    for users_chunk in chunked(gen_users_data(20), 10):
        tasks.append(asyncio.create_task(insert_users(pool, users_chunk)))

    await asyncio.gather(*tasks)
    await pool.close()

if __name__ == '__main__':
    asyncio.run(main())