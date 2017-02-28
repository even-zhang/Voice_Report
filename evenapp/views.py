from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import codecs
import os
import itertools
import re
import time

# Create your views here.


def time_split(input_data):
    mins = r'(((\d{1,2}|(半|一刻)|(十|一|二|三|四|五|六|七|八|九)(十)*(一|二|三|四|五|六|七|八|九)*)(分)*)*)'
    hours = r'((\d{1,2}|(十|一|二|三|四|五|六|七|八|九|两)(十)*(一|二|三|四|五|六|七|八|九|两)*)(:|点过|点整|点差|点零|点左右|点钟|点))'
    date = r'((\d{4}年)*(\d{1,2}月)\d{1,2}(日|号))'
    days = r'(今天|昨天|前天|明天|后天|刚才|刚刚)'
    section = r'(早上|中午|下午|傍晚|凌晨|晚上)'
    tim = date + '|' + days + '|' + section + '|' + (hours + mins)
    jud = re.search(tim, input_data)
    times = ''
    data = input_data
    while jud:
        times = times + re.search(tim, data).group()
        data = data.replace(re.search(tim, data).group(), '')
        jud = re.search(tim, data)
    now = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    y = re.search(r'\d{4}-', now).group()
    y = int(re.sub(r'-', '', y))
    m = re.search(r'-\d{1,2}-', now).group()
    m = int(re.sub(r'-', '', m))
    d = re.search(r'-\d{1,2}\s', now).group()
    d = int(re.sub(r'-', '', d))
    h = re.search(r'\d{1,2}:', now).group()
    h = re.sub(r':', '', h)
    mi = re.search(r':\d{1,2}', now).group()
    mi = re.sub(r':', '', mi)
    ye = re.search(date, times)
    da = re.search(days, times)
    se = re.search(section, times)
    hm = re.search((hours+mins), times)
    if ye:
        input_data = input_data.replace(re.search(tim, input_data).group(), '')
    if hm:
        times = re.sub(r'一刻', r'15', times)
        times = re.sub(r'一', '1', times)
        times = re.sub(r'二', '2', times)
        times = re.sub(r'三', '3', times)
        times = re.sub(r'四', '4', times)
        times = re.sub(r'五', '5', times)
        times = re.sub(r'六', '6', times)
        times = re.sub(r'七', '7', times)
        times = re.sub(r'八', '8', times)
        times = re.sub(r'九', '9', times)
        times = re.sub(r'十', '10', times)
        times = re.sub(r'零', '0', times)
        times = re.sub(r'点过|点钟|点左右|点整', r':00', times)
        times = re.sub(r'点', r':', times)
        times = re.sub(r'半', r'30', times)
        times = re.sub(r'分', '', times)
        ho = re.search(r'\d+?:', times)
        ms = re.search(r':\d+', times)
        if ho:
            ho = ho.group()
            if len(ho) == 2:
                times = re.sub(r'\d+?:', ('0' + ho), times)
            if len(ho) == 4:
                times = re.sub(r'\d+?:', (ho[0]+ho[2:]), times)
            if len(ho) == 5:
                times = re.sub(r'\d+?:', (ho[0] + ho[3:]), times)
        if ms:
            ms = ms.group()
            if len(ms) == 2:
                times = re.sub(r':\d+', (ms[0] + '0' + ms[1]), times)
            if len(ms) == 4:
                times = re.sub(r':\d+', (ms[0:2]+ms[3]), times)
            if len(ms) == 5:
                times = re.sub(r':\d+', (ms[0] + ms[3:]), times)
            if len(ms) == 6:
                times = re.sub(r':\d+', (ms[0] + ms[3] + ms[5]), times)
            if len(ms) == 7:
                times = re.sub(r':\d+', (ms[0] + ms[3] + ms[6]), times)

    if da:
        times = re.sub(r'今天', str(str(y) + '年' + str(m) + '月' + str(d) + '日'), times)
        times = re.sub(r'刚才', str(str(y) + '年' + str(m) + '月' + str(d) + '日' + h + ':' + mi), times)
        times = re.sub(r'刚刚', str(str(y) + '年' + str(m) + '月' + str(d) + '日' + h + ':' + mi), times)
        times = re.sub(r'昨天', str(str(y) + '年' + str(m) + '月' + str(d - 1) + '日'), times)
        times = re.sub(r'前天', str(str(y) + '年' + str(m) + '月' + str(d - 2) + '日'), times)
        times = re.sub(r'明天', str(str(y) + '年' + str(m) + '月' + str(d + 1) + '日'), times)
        times = re.sub(r'后天', str(str(y) + '年' + str(m) + '月' + str(d + 2) + '日'), times)
    elif ('今天' or '昨天' or '前天' or '明天' or '后天' not in times) and (not ye) and ('早上' or '中午' or '下午' or '傍晚' or '凌晨' or '晚上' in times):
        times = str(str(y) + '年' + str(m) + '月' + str(d) + '日') + times
    elif '年' not in times:
        times = str(str(y) + '年') + times
    if se and (not hm):
        times = re.sub(r'早上', r'08:00', times)
        times = re.sub(r'中午', r'12:00', times)
        times = re.sub(r'下午', r'16:00', times)
        times = re.sub(r'傍晚', r'20:00', times)
        times = re.sub(r'晚上', r'22:00', times)
        times = re.sub(r'凌晨', r'00:00', times)
    return input_data, times


def character_split(input_data, output_file):
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for word in input_data.strip():
         word = word.strip()
         if word:
            output_data.write(word + "\tB\n")
    output_data.write("\n")
    output_data.close()


def Tagging_sentence():
    os.chdir(r'C:\Users\User\Desktop\NLP\demo')
    os.system('crf_test -m model_new test>tag')


def Tagging_time():
    os.chdir(r'C:\Users\User\Desktop\NLP\demo')
    os.system('crf_test -m model_timeadd test.txt>tag_time.txt')


def character_2_word(input_file, address, event):
    input_data = open(input_file, 'r', encoding="utf-8", errors='ignore')
    #input_data = codecs.open(input_file, 'r', 'utf-8')
    for line in input_data:
        a = len(line)
        if a > 2:
            char_tag_pair = line.strip().split('\t')
            char = char_tag_pair[0]
            tag = char_tag_pair[2]
            if tag == 'B':
                address.append(char)
            elif tag == 'M':
                address.append(char)
            elif tag == 'E':
                address.append(char)
            elif tag == 'S':
                address.append(char)
            else:
                event.append(char)
    input_data.close()
    return address, event


def time_address_split(time, address, a):
    character_split(a, output_file=r"C:\Users\User\Desktop\NLP\demo\test.txt")
    Tagging_time()
    input_data = codecs.open(r"C:\Users\User\Desktop\NLP\demo\tag_time.txt", 'r', 'utf-8')
    for line in input_data.readlines():
        a = len(line)
        if a == 7:
            char_tag_pair = line.strip().split('\t')
            char = char_tag_pair[0]
            tag = char_tag_pair[2]
            if tag == 'B':
                address.append(char)
            elif tag == 'M':
                address.append(char)
            elif tag == 'E':
                address.append(char)
            elif tag == 'S':
                address.append(char)
            else:
                time.append(char)
    input_data.close()
    return address, time


def del_time(a):
    mins = r'(((\d{1,2}|(十|一|二|三|四|五|六|七|八|九)(十)*(一|二|三|四|五|六|七|八|九)*|(半|一刻))(分)*)*)'
    hours = r'((\d{1,2}|(十|一|二|三|四|五|六|七|八|九|两)(十)*(一|二|三|四|五|六|七|八|九|两)*)(:|点过|点整|点差|点零|点左右|点钟|点))'
    date = r'((\d{4}年)*(\d{1,2}月)\d{1,2}(日|号))'
    days = r'(今天|昨天|前天|明天|后天)'
    section = r'(早上|中午|下午|傍晚|凌晨|晚上)'
    tim = date + '|' + days + '|' + section + '|' + (hours + mins)
    jud = re.search(tim, a)
    times = ''
    while jud:
        times = times + '，' + re.search(tim, a).group()
        a = a.replace(re.search(tim, a).group(), '')
        jud = re.search(tim, a)
    return a


def data_split(input_data):
    address = []
    event = []
    test_file = open(r"C:\Users\User\Desktop\NLP\demo\test", "w", encoding="utf-8", errors='ignore')
    output_file = r"C:\Users\User\Desktop\NLP\demo\test"
    input_file = r"C:\Users\User\Desktop\NLP\demo\tag"
    input_data = re.sub(',|，|。', '', input_data)
    input_data, t = time_split(input_data)
    character_split(input_data, output_file)
    Tagging_sentence()
    character_2_word(input_file, address, event)
    a = "".join(itertools.chain(address))
    a = del_time(a)
    e = "".join(itertools.chain(event))
    return a, e, t


def index(request):
    input_data = request.POST['case']
    address, event, times = data_split(input_data)
    d = {'Time': times, 'Address': address, 'Event': event}
    return JsonResponse(d, json_dumps_params={'ensure_ascii': False},)
