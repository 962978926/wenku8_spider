import requests
from bs4 import BeautifulSoup as bs
import json
from multiprocessing import Pool

# TODO:去重，过滤空白符
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
}


def get_dict(number):
    url = 'https://www.wenku8.net/book/{}.htm'.format(number)
    r = requests.get(url, headers=headers)
    html = r.text.encode('latin-1').decode('GBK')
    soup = bs(html, 'lxml')
    detials = soup.find('div', id="content")
    name = detials.find('span', style="font-size:16px; font-weight: bold; line-height: 150%").select('b')[0].get_text()
    img = detials.img.attrs['src']
    wenku = detials.findAll('td', width="20%")[0].get_text()
    author = detials.findAll('td', width="20%")[1].get_text()
    state = detials.findAll('td', width="20%")[2].get_text()
    if(len(detials.findAll('td', width="20%")) > 3):
        last_update = detials.findAll('td', width="20%")[3].get_text()
        length = detials.findAll('td', width="20%")[4].get_text()
        jj = detials.findAll('span', style="font-size:14px;")[1].get_text()
    else:
        last_update = '未知'
        length = '未知'
        jj = detials.findAll('span', style="font-size:14px;")[0].get_text()
    out = "".join(jj.split())
    yd = detials.find(text=(u'小说目录')).parent.attrs['href']
    dic = {
        '书名': name,
        '文库': wenku,
        '作者': author,
        '状态': state,
        '简介': out,
        '更新时间': last_update,
        '全文长度': length,
        '图片链接': img,
        '阅读链接': yd
    }
    return dic


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(n):
    for number in range(300 * n, 300 * (n + 1) - 1):
        try:
            g = get_dict(number)
            print(g)
            write_to_file(g)
        except:
            pass


if __name__ == '__main__':
    p = Pool()
    p.map(main, [i for i in range(10)])
    p.close()
    p.join()
