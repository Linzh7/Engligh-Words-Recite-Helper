import csv
import random
import requests
from playsound import playsound

# filepath
path = '.'


# get translated text from baidu
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


# print to screen
def prints(element, degree):
    print('\033[1;32m  ', element[2], '\033[0m')
    print('\033[1;34m   熟练度:', element[3], '+', degree, '\033[0m')
    print()


# read and test
def do(ls):
    random.shuffle(ls)
    for element in ls:
        # skip null element
        if element[1] == '':
            continue
        print('\033[1;33m', element[1], '\033[0m', end='           ')
        playsound(path + '/Audio/' + element[1] + '.mp3')
        know = input()
        # get input
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


# main
ls = []
donels = []
# read from file
with open(path + '/单词.csv', 'r') as f:
    lines = csv.reader(f)
    for i in lines:
        ls.append(i)

# select mode
mode = input("\033[1;35mMode: \033[0m")
# main mode
if mode in ['0', '']:
    # print words amount
    print('\033[1;35msum:', len(ls), '\033[0m')
    # exam
    try:
        do(ls)
    except:
        print("Error: 001")
    # save unfinished words
    with open(path + '/单词.csv', 'w') as f:
        writer = csv.writer(f)
        for element in ls:
            if int(element[3]) < 3:
                writer.writerow(element)
            else:
                donels.append(element)
    # save finished words
    with open(path + '/完成单词.csv', 'a+') as f:
        writer = csv.writer(f)
        for element in donels:
            writer.writerow(element)
    print("\033[1;33m[System] Saved.\033[0m")

# modify mode
elif mode == '9':
    # download audio
    j = 1
    for i in ls:
        print("{}: {}".format(j, i[1]))
        res = requests.get('http://dict.youdao.com/dictvoice?type=0&audio=' +
                           i[1])
        music = res.content
        with open(path + '/Audio/' + i[1] + '.mp3', 'wb') as file:
            file.write(res.content)
            file.flush()
        j += 1
    print('\033[1;33m[System] MP3 files Done.\033[0m')

    # translate and format
    with open(path + '/单词.csv', 'w') as f:
        writer = csv.writer(f)
        for element in ls:
            if element[3] == '':
                element[3] = '0'
            if element[0] == '':
                element[0] = '0'
            try:
                element[2] = trans(element[1])
                print(element[1], element[2])
            except:
                element[2] = 'NULL'
                print('\033[1;33m[System]Error: ', element[1], '\033[0m"')
            writer.writerow(element)
    print('\033[1;33m[System] Translates Done.\033[0m')
