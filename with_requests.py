import random
import json
import time
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Authorization': '',
    'X-Super-Properties': '',
    'X-Discord-Locale': 'en-US',
    'X-Discord-Timezone': 'America/New_York',
    'X-Debug-Options': 'bugReporterEnabled',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
}

def read_json_file(path):
    with open(path, 'r', encoding = 'utf-8') as file:
        return json.loads(file.read())

def write_json_file(path, data):
    with open(path, 'w', encoding = 'utf-8') as file:
        file.write(json.dumps(data, indent = 4))

def get_messages(guild_id, author_id, offset):
    response = requests.get(
        url = f'https://discord.com/api/v9/guilds/{guild_id}/messages/search',
        params = { 'author_id': author_id, 'offset': offset },
        headers = headers,
        timeout = 60
    )

    messages = {}

    for message in json.loads(response.text)['messages']:
        messages[message[0]['id']] = {
            'content': message[0]['content'],
            'timestamp': message[0]['timestamp']
        }

    return messages

def main():
    path = ''
    guild_id = ''
    author_id = ''
    offset = 0

    stop = False
    while not stop:
        try:
            messages = get_messages(guild_id, author_id, offset)
        except:
            offset += 25
            time.sleep(random.randint(2, 3))
            continue

        storage = read_json_file(path)

        for message_id, message in messages.items():
            storage[message_id] = message
            print(f'Offset: {offset}, Written: {message['content']}')

        write_json_file(path, storage)

        offset += 25
        time.sleep(random.randint(2, 3))

main()
