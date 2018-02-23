import requests
import re
import json
from multiprocessing import Pool
from requests.exceptions import RequestException

def  get_page(url):
    try:
        respone = requests.get(url)
        if respone.status_code == 200:
            respone = respone.text
        return respone
    except RequestException:
        return ('hello')


def prase_page(html):
    parrtern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',
        re.S)
    result = re.findall(parrtern, html)

    for i in result:
        # dic {'index': i[0], 'image': i[1], 'name': i[2], 'author': i[3].strip()[3:], 'time': i[4],
        #        'score': i[5] + i[6]}
       yield {
            'index':i[0],
            'image':i[1],
            'name': i[2],
            'author': i[3].strip()[3:],
            'time': i[4],
            'score': i[5] + i[6]
       }

def write_file(list):
    with open('json.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(list, ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_page(url)
    for i in prase_page(html):
        print(i)
        write_file(i)



if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(9)])