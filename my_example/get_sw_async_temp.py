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
    print(response_json['name'])
    await session.close()
    return response_json


async def main():

    for person_ids_chunk in more_itertools.chunked(range(1, 20), 10):
        list_of_task = []
        for person_id in person_ids_chunk:
            task = asyncio.create_task(get_person(person_id))
            list_of_task.append(task)
        task_results = await asyncio.gather(*list_of_task)



start = time.time()
asyncio.run(main())
print('Время работы ', time.time() - start)