import csv
import random
import requests
from playsound import playsound

path = '.'


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


def prints(element, degree):
    print('\033[1;32m  ', element[2], '\033[0m')
    print('\033[1;34m   熟练度:', element[3], '+', degree, '\033[0m')
    print()


def do(ls):
    random.shuffle(ls)
    for element in ls:
        if element[1] == '':
            continue
        print('\033[1;33m', element[1], '\033[0m', end='           ')
        playsound(path + '/Audio/' + element[1] + '.mp3')
        know = input()
        if know in ['\'', '']:
            prints(element, 0)
        elif know in [';', '.']:
            prints(element, 1)
            element[3] = int(element[3]) + 1
        elif know in [';;', '..']:
            prints(element, 2)
            element[3] = int(element[3]) + 2
        else:
            prints(element, 0)
            break


ls = []
donels = []
with open(path + '/单词.csv', 'r') as f:
    lines = csv.reader(f)
    for i in lines:
        ls.append(i)

mode = input("\033[1;35mMode: \033[0m")
if mode in ['0', '']:
    print('\033[1;35msum:', len(ls), '\033[0m')
    try:
        do(ls)
    except:
        print("Error: 001")
    with open(path + '/单词.csv', 'w') as f:
        writer = csv.writer(f)
        for element in ls:
            if int(element[3]) < 3:
                writer.writerow(element)
            else:
                donels.append(element)
    with open(path + '/完成单词.csv', 'w+') as f:
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
        with open(path + '/Audio/' + i[1] + '.mp3', 'wb') as file:
            file.write(res.content)
            file.flush()
        j += 1
    print('\033[1;33mSystem: MP3 Done.\033[0m')
    with open(path + '/单词.csv', 'w') as f:
        writer = csv.writer(f)
        for element in ls:
            try:
                element[2] = trans(element[1])
                print(element[1], element[2])
            except:
                element[2] = 'NULL'
                print('\033[1;33mSystem: Error, ', element[1], '\033[0m"')
            writer.writerow(element)
    print('\033[1;33mSystem: Translates Done.\033[0m')
