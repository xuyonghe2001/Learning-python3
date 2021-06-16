import os
import concurrent
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import lxml

def header(referer):
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': '{}'.format(referer),
    }
    return headers

hd = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
    }

def request_page(url):
    try:
        response = requests.get(url, headers=hd)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def get_page_urls():
    for i in range(1, 2):

        baseurl = 'https://www.mzitu.com/page/{}'.format(i)
        html = request_page(baseurl)
        soup = BeautifulSoup(html, 'lxml')
        list = soup.find(class_='postlist').find_all('li')
        urls = []
        for item in list:
            url = item.find('span').find('a').get('href')
            print('页面链接：%s ' % url)
            urls.append(url)

    return urls

def download_pic(title, image_list):
    os.mkdir(title)
    j =1
    for item in image_list:
        filename = '%s/%s.jpg' % (title, str(j))
        print('downloading...%s : NO.%s' % (title, str(j)))
        with open(filename, 'wb') as f:
            img = requests.get(item, headers=header(item)).content
            f.write(img)
        j += 1

def download(url):
    html = request_page(url)
    soup = BeautifulSoup(html, 'lxml')
    total = soup.find(class_='pagenavi').find_all('a')[-2].find('span').string
    title = soup.find('h2').string
    image_list = []

    for i in range(int(total)):
        html = request_page(url + '/%s' %(i+1))
        soup = BeautifulSoup(html, 'lxml')
        img_url = soup.find('img').get('src')
        image_list.append(img_url)

    download_pic(title, image_list)




if __name__ == '__main__':
    list_page_urls = get_page_urls()
    for item in list_page_urls:
        download(item)