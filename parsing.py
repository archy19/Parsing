import requests
import bs4
import random


def search_web(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/79.0.3945.136 YaBrowser/20.2.1.248 Yowser/2.5 Safari/537.36', 'Accept-Language':
                   'ru-RU'}
    try:
        s1 = requests.get(url, headers=headers)
    except Exception as e:
        print('Произошла ошибка при входе в интернет')
        print(e)
        rt = input("Для продолжения нажмите Enter: ")
    if int(s1.status_code) == 200:
        wq = True
    else:
        print('Произошла ошибка ' + str(s1.status_code) + ' получения данных с сайта:')
        wq = False
    if wq:
        b1 = bs4.BeautifulSoup(s1.text, "html.parser")
        return b1
    else:
        return False


def get_text(data):
    text = data.find('div', class_="post__body post__body_full").getText()
    elems_pre = data.select('div[id="post-content-body"] pre')
    if len(elems_pre) > 0:
        for k in range(0, len(elems_pre)):
            text = text.replace(elems_pre[k].getText(), '')
    text = text.replace('\v', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('\f', ' ')
    text = text.replace('\n', ' ')
    return text


file = open('parsing.txt', 'a', encoding='utf-8')
i = 1
a = True
while a:
    try:
        ur = 'https://habr.com/ru/post/'
        numb = random.randrange(526500)
        url = ur + str(numb) + '/'
        data = search_web(url)
        if data:
            file.write('link' + str(i) + ': ' + url + '\n')  # запись ссылки
            file.write('title' + str(i) + ': ' + data.find('h1').getText().strip() + '\n')  # запись названия
            text = get_text(data)
            file.write('body' + str(i) + ': ' + text + '\n')  #
            tegi = data.find('div', class_="post__wrapper").find('dl').find('ul').find_all('li')
            for j in range(len(tegi)):
                tag = data.find('div', class_="post__wrapper").find('dl').find('ul').find_all('li')[j].getText().strip()
                if j == 0 and len(tegi) > 1:
                    file.write('tags' + str(i) + ': ' + tag + '; ')
                elif j == 0 and len(tegi) == 1:
                    file.write('tags' + str(i) + ': ' + tag + '.')
                elif j == len(tegi)-1:
                    file.write(tag + '.')
                else:
                    file.write(tag + '; ')
            file.write('\n')
            file.write('\n')
            i += 1
            if i == 56:
                a = False
        else:
            print('нет такой статьи')
    except Exception as e:
        print(e)
file.close()