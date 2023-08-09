import re
import os
import json
import requests
import subprocess
from nodejs.bindings import node_run

current_dir = os.path.dirname(os.path.realpath(__file__))


def douban_movie_search(keyword):
    url = f'https://search.douban.com/movie/subject_search?search_text={keyword}&cat=1002'
    response = requests.get(url=url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"})

    data = re.findall(r'window.__DATA__ = "(.*?)";', response.text)
    if len(data) == 0:
        return
    data = data[0]
    # print(data)

    with open(f'{current_dir}/douban.js', 'r') as douban_js:
        with open(f'{current_dir}/douban_v2.js', 'w+') as w:
            w.write(douban_js.read().replace('{douban_base64_encode}', data))

    douban_v2_js_path = f"{current_dir}/douban_v2.js"
    # print(douban_v2_js_path)
    stderr, stdout = node_run(douban_v2_js_path, data)

    data = json.loads(stdout)
    # print(stderr, stdout)
    # print(data)
    os.remove(douban_v2_js_path)

    exist_all_keys = set()

    result_data = []
    for one in data['payload']['items']:
        if type(one) is dict:
            for k in one.keys():
                exist_all_keys.add(k)

        data = {}
        if 'title' not in one or 'rating' not in one:
            continue
        # for k in ['abstract', 'abstract_2', 'title', 'rating']:
        for k in ['title', 'rating']:
            data[k] = one[k]
        # print(data['title'], data['rating']['value'])

        result_data.append({
            'title': data['title'], 'scores': data['rating']['value'],
        })

    return result_data
    # print(exist_all_keys)


if __name__ == '__main__':
    keyword = '权力的游戏'
    douban_movie_search(keyword)
