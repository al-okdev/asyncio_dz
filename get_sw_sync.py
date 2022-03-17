import requests
import time


url = 'https://swapi.dev/api'

def get_person(person_id):

    return requests.get(f'{url}/people/{person_id}').json()


def main():
    for person_id in range(1, 10):
        print(get_person(person_id))

start = time.time()
main()
print('Время работы ', time.time() - start)