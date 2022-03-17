import asyncio
import aiohttp
import time
import more_itertools

url = 'https://swapi.dev/api'

async def get_person(person_id):
    print(person_id)
    session = aiohttp.ClientSession()
    response = await session.get(f'{url}/people/{person_id}')
    response_json = await response.json()
    print(response_json)
    await session.close()
    return response_json


async def get_people(people_ids):
    tasks = [asyncio.create_task(get_person(person_id)) for person_id in people_ids]
    for task in tasks:
        tasks_result = await task
        yield tasks_result


async def main():

    for person_ids_chunk in more_itertools.chunked(range(1, 100), 10):
        async for person in get_people(person_ids_chunk):
            print(person)


start = time.time()
asyncio.run(main())
print('Время работы ', time.time() - start)