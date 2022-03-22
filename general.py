import os
import pandas as pd
import string

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)
def save_info_file(project_name, df):
    info_file_path_csv = os.path.join(project_name, (project_name +'_info.csv'))
    info_file_path_xlsx = os.path.join(project_name, (project_name +'_info.xlsx'))

    if not os.path.isfile(info_file_path_csv):
        df.to_csv(info_file_path_csv)
    if not os.path.isfile(info_file_path_xlsx):
        df.to_excel(info_file_path_xlsx, sheet_name=str(project_name), index=False)

def create_comment_file(project_name, video_title):
    comment_file = os.path.join(project_name, (video_title + '_comment.txt'))
    if not os.path.isfile(comment_file):
        with open(comment_file, 'w') as f:
            f.write('')
            f.close()
#def store_info(data, file_name):
def set_to_file(data, file_name):
    with open(file_name, 'w') as f:
        for url in data:
            f.write(url + '\n')

def store_data(data, file_name):
    with open(file_name, 'wb') as f:
        for com in data:
            f.write(com.encode("utf8") + b'\n')

def parse_string(item):
    item = item.strip(string.ascii_letters)
    item = item.replace(",", '').replace(" ", '')
    item = int(item)
    return item

def duration_to_min(duration):
    separation = duration.split(':')

    if len(separation) > 2:
        time_min = int(separation[0])*60 + int(separation[1]) + int(separation[2])/60
    else:
        time_min = int(separation[0]) + int(separation[1]) / 60

    time_min = float("{:.2f}".format(time_min))
    return(time_min)


def n_sub_to_int(item):
    item = item.split()
    item = item[0]
    if item[-1] is ('K' or 'k'):
        item = int(item[:-1])
        item = float(item) * 1000
    elif item[-1] is ('M' or 'm'):
        item = item[:-1]
        item = float(item) * 1000000

    item = int(item)

    return item

def clean_keywords(keywords, channelname):
    component = channelname.split()
    for n in range(len(keywords)):
        for n2 in range(len(component)):
            keywords[n] = keywords[n].replace(component[n2], '')
            keywords[n] = keywords[n].replace(' ', '')
    return [x for x in list(dict.fromkeys(keywords)) if x]

def keywords_to_search_url(keywords):
    url_list = []
    for word in keywords:
        url = 'https://www.youtube.com/results?search_query=' + word
        url_list.append(url)
    return url_list
