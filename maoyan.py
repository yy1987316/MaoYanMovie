import requests
import time
import json
import re

def getPage(url):
    """
    获取1个页面
    :param url:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except:
        return None

def parsePage(html):
    """
    解析页面
    :param html:
    :return:
    """
    pattern = re.compile(r'<dd.*?board-index.*?>(.*?)</i>.*?<img data-src="(.*?)".*?name.*?<a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>', re.S)
    movies = pattern.findall(html)
    for movie in movies:
        yield {
            'index': movie[0],
            'image': movie[1],
            'name': movie[2],
            'actor': movie[3].strip()[3:] if len(movie[3]) > 3 else '',
            'time': movie[4][5:] if len(movie[4]) > 5 else '',
            'score': movie[5] + movie[6]
        }

def saveFile(file_name, line):
    """
    保存文件
    :param file_name:
    :param line:
    :return:
    """
    with open(file_name, 'a', encoding='utf-8') as f:
        print(json.dumps(line, ensure_ascii=False))
        f.write(json.dumps(line, ensure_ascii=False) + '\n')

def main(offset):
    """
    主流程
    :param offset:
    :return:
    """
    url = 'https://maoyan.com/board/4?offset={}'.format(offset)
    file_name = 'result.txt'
    html = getPage(url)
    if html:
        for movie in parsePage(html):
            saveFile(file_name, movie)


if __name__ == '__main__':
    for i in range(10):
        offset = i * 10
        main(offset)
        time.sleep(1)