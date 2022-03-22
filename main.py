# 20220302 - 20220401
# To crawl information and comment from given list of links
# Store the basic video information in a csv file
# Store video comments of each video in separated txt file

from crawler_webdriver import *
from general import *
import pandas as pd
import openpyxl
import os

PROJECT_NAME = 'liziqi_top_10'
create_project_dir(PROJECT_NAME)



# if __name__ == "__main__": # so when this is imported as another file, it will not be triggered
# I don't really need this
urls = [
    "https://www.youtube.com/watch?v=FWMIPukvdsQ",
    "https://www.youtube.com/watch?v=_jUJrIWp2I4",
    "https://www.youtube.com/watch?v=QHTnuI9IKBA",
    "https://www.youtube.com/watch?v=kgEgOi32CE0",
    "https://www.youtube.com/watch?v=LTejJnrzGPM",
    "https://www.youtube.com/watch?v=hR4DiU8wcVk",
    "https://www.youtube.com/watch?v=IL1tDfWDbsA",
    "https://www.youtube.com/watch?v=wUJ-57SAE5A",
    "https://www.youtube.com/watch?v=rJSZfrJFluw",
    "https://www.youtube.com/watch?v=oi38cQMORQY",
]


##### get info of ten provided link
#df = ScrapInfo(urls)
#save_info_file(PROJECT_NAME, df)
#print("csv and xlsx info files are created")

### get comments of ten provided link and store in seperated file
'''
for url in urls:
    start_time = time.time()
    print("\n\n-------- Start scrapping " + url)
    video_id = url[len(url)-11:len(url)]
    ScrapComment(url, PROJECT_NAME, video_id)
    print("---- Time used is %s seconds" % (time.time() - start_time))
'''

#### get keywords

info_file = os.path.join(os.getcwd(), 'liziqi_top_10\liziqi_top_10_info.csv')
df = pd.read_csv(info_file)

keyword_list = list()
for keywords in df['keywords']:
    keywords = keywords.split(',')
    for keyword in keywords:
        keyword_list.append(keyword)
keyword_list = clean_keywords(keyword_list, channelname=df.iloc[1, 1])
# regax should be used to remove all LIZIQI
# I am gonna do it mannualy before I learn it
'''
for i in range(len(keyword_list)):
    print(i, end=" ")
    print(keyword_list[i])
'''
selection = [4, 5, 8, 9, 10, 11, 12,13, 14, 19, 22, 23, 24, 25, 26, 28, 29, 30, 31, 35, 36, 37, 38, 43, 45, 46, 47, 48, 49,
             50, 53, 54, 55, 56, 57, 58, 59, 60, 61]
keyword_list_filtered = []
for i in range(len(keyword_list)):
    if i in selection:
        keyword_list_filtered.append(keyword_list[i])

print(keyword_list_filtered)
#### get all related links
related_url_list = keywords_to_search_url(keyword_list_filtered)
'''
if os.path.isfile('related_url_set.txt'):
    print('existing related url file detected')
    search_results_url = []
    with open('related_url_set.txt') as f:
        lines = f.readlines()
    for url in lines:
        search_results_url.append(url[:len(url) - 2])
else:
'''
search_results_url = search_and_grab_url(related_url_list[2:4])
print(search_results_url)
#search_and_grab_url(url_list)

#### get all comments of related links and store in seperated files
PROJECT_NAME2 = 'liziqi_keywords_search_comments'
create_project_dir(PROJECT_NAME2)
for url in search_results_url:
    start_time = time.time()
    print("\n\n-------- Start scrapping " + url)
    video_id = url[len(url) - 11:len(url)]
    path = os.path.join(PROJECT_NAME2, (video_id + '_comment.txt'))
    if not os.path.isfile(path):
        ScrapComment(url, PROJECT_NAME2, video_id)
    else:
        print(video_id + "file already exist")
    print("---- Time used is %s seconds" % (time.time() - start_time))