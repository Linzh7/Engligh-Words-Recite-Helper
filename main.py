import csv
import random
import requests
from playsound import playsound


def trans(word):
    url = 'https://fanyi.baidu.com/sug'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
        'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;'
        'q=0.9,image/webp,*/*;q=0.8'
    }
    Form_data = {'kw': word}
    response = requests.post(url, data=Form_data, headers=headers)
    res = response.json()['data'][0]['v']
    return res


def prints(element, tran, degree):
    print('\033[1;32m  ', tran, '\033[0m')
    print('\033[1;34m   熟练度:', element[3], '+', degree, '\033[0m')
    print()


def do(ls):
    random.shuffle(ls)
    for element in ls:
        print('\033[1;33m', element[1], '\033[0m', end='           ')
        playsound('/Users/Linzh/Local/English/' + element[1] + '.mp3')
        try:
            tran = trans(element[1])
            element[2] = tran
        except:
            tran = 'ERROR'
        know = input()
        if know in ['\'', '']:
            prints(element, tran, 0)
        elif know in [';', '.']:
            prints(element, tran, 1)
            element[3] = int(element[3]) + 1
        elif know in [';;', '..']:
            prints(element, tran, 2)
            element[3] = int(element[3]) + 2
        else:
            break


ls = []
donels = []
with open('/Users/Linzh/Local/English/单词.csv', 'r') as f:
    lines = csv.reader(f)
    for i in lines:
        ls.append(i)

mode = input("\033[1;35mMode: \033[0m")
if mode == '0':
    print('\033[1;35msum:', len(ls), '\033[0m')
    try:
        do(ls)
    except:
        print("Error!")
    with open('./单词.csv', 'w') as f:
        writer = csv.writer(f)
        for element in ls:
            if int(element[3]) < 3:
                writer.writerow(element)
            else:
                donels.append(element)
    with open('./完成单词.csv', 'w') as f:
        writer = csv.writer(f)
        for element in donels:
            writer.writerow(element)
    print("\033[1;33mSystem: Saved.\033[0m")

elif mode == '9':
    j = 0
    for i in ls:
        print("{}: {}".format(j, i[1]))
        res = requests.get('http://dict.youdao.com/dictvoice?type=0&audio=' +
                           i[1])
        music = res.content
        with open('./' + i[1] + '.mp3', 'wb') as file:
            file.write(res.content)
            file.flush()
        j += 1
    print('done.')
