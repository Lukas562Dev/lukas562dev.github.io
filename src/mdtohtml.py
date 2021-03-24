import requests

api_url = 'https://api.github.com/markdown'

def md_to_html(md):
    json = {
        'text': md
    }
    res = requests.post(api_url, json=json)

    return res.text

if __name__ == "__main__":
    print('This file is supposed to be used as a library')