import requests


def fox():
    url = 'https://randomfox.ca/floof'

    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get('image')
    else:
        return None

if __name__ == '__main__':
    print(fox())