# for webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

# for clicking the ad
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# for getting html elements, can be don using selenium
from bs4 import BeautifulSoup

# for creating, storing, deleting files
from general import *

# to get extration time
from datetime import datetime

option = webdriver.ChromeOptions()
option.add_argument("--headless")
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=option)

def ScrapInfo(urls):

    option = webdriver.ChromeOptions()
    # option.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    df = pd.DataFrame(columns=['channel', 'n_subscribe', 'uploaded_date',
                               'title', 'translated_title', 'n_view', 'n_like',
                               'duration_min', 'keywords', 'url',
                               'photo_link', 'extraction_date', 'n_comment'])

    for n in range(len(urls)):
        info = []
        print('Crawling url number ' + str(n+1) + '  ' + urls[n])
        driver.get(urls[n])
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # scrip the channel name
        channel_name = soup.select_one('#meta #container #text-container a')
        info.append(channel_name.text)

        # scrip the n_subscribe
        sub_count = soup.select_one('#meta #owner-sub-count')
        sub_count_int = n_sub_to_int(sub_count.text)
        info.append(sub_count_int)


        # scrip the uploaded_date
        uploaded_date = soup.select_one('#info-strings.style-scope > yt-formatted-string').text
        info.append(uploaded_date)

        # scrap the true title
        title_meta = soup.find_all('meta', {'name': 'title'})  # I am not sure how should this variable be named....
        true_title = title_meta[0]['content']
        info.append(true_title)

        # scrip the translated title
        title_text_div = soup.select_one('#info h1')
        info.append(title_text_div.text)

        # scrip the n_view
        view_count = soup.select_one('span.view-count')
        n_view = parse_string(view_count.text)
        info.append(n_view)

        # scrip the n_like
        n_like_div = soup.select_one('a > yt-formatted-string#text.style-scope')
        n_like = parse_string(n_like_div['aria-label'])
        info.append(n_like)

        # scrip the video duration
        # the ad need to be skipped, otherwise the program will scrap the duration of the ad
        # hey future PP, if you wanna keep the detection going, we can driver.get(www.youtube.com) and add a while True, try: loop

        media_player_div = soup.select_one('#movie_player')

        print('Detecting if ad is showing')
        # I tried to use a while loop in case if there is more than one ad, but I failed, so I used
        while 'ad-showing' in soup.select_one('#movie_player')['class']:
            print('ad is detected, waiting to skip')
            wait = WebDriverWait(driver, 30)

            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ytp-ad-skip-button-container")))
            element.click()
            time.sleep(3)

            # renew the soup so to see whether there are more ad
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            print("ad is skipped!")


        duration = soup.select_one('span.ytp-time-duration').text
        time_min = duration_to_min(duration)
        info.append(time_min)

        # scrape keywords
        keywords_meta = soup.find_all('meta', {'name': 'keywords'})
        keywords = keywords_meta[0]['content']
        info.append(keywords)

        # scrape short url
        shortlink_meta = soup.find_all('link', {'rel': 'shortlinkUrl'})
        shortlink = shortlink_meta[0]['href']
        info.append(shortlink)

        # scrape the photo link
        photo_meta = soup.find_all('link', {'rel': 'image_src'})
        photo_link = photo_meta[0]['href']
        info.append(photo_link)

        # add extraction_date
        extracted_at = datetime.today().strftime('%Y-%m-%d')
        info.append(extracted_at)

        # scrip the n_comment
        # scroll so that the number of comments appear
        driver.execute_script(f"window.scrollTo(0, 500)")  # so that the count of comment appear
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        comment_count = soup.select_one('h2#count > yt-formatted-string > span').text
        info.append(parse_string(comment_count))

        # scrap video description
        # a few descriptions do not generate a lot of insights, so I will just get rid of them
        #video_description = soup.select_one("#container #content")
        #info.append(video_description.text)


        print('Successfully scraped url number ' + str(n))
        df.loc[n, ] = info

    return df



def search_and_grab_url(url_list):
    related_url_set = set()

    # for loop
    for url in url_list:
        print("Scarping " + url)
        driver.get(url)
        driver.execute_script(f"window.scrollTo(0, 500)")  # so that the count of comment appear
        time.sleep(2)
        driver.execute_script(f"window.scrollTo(0, 1000)")
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title_div = soup.select("h3 > a")
        for title in title_div:
            href = 'https://www.youtube.com' + title['href']
            related_url_set.add(href)
    set_to_file(related_url_set, 'related_url_set.txt')
    return related_url_set


def ScrapComment(url, PROJECT_NAME, vid_title):
    create_comment_file(PROJECT_NAME, vid_title)
    comment_file = PROJECT_NAME + '/' + vid_title + '_comment.txt'

    #option = webdriver.ChromeOptions()
    #option.add_argument("--headless")
    #driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)

    # solve the incompatibility between webdriver and the browser version
    # create a driver object
    driver.get(url)
    time.sleep(4)  # for loading the content?
    prev_h = 0
    nScroll = 1
    # set to True to get all comments
    # set to 3000 for testing
    #  prev_h <= 3000
    while True:
        height = driver.execute_script("""
                function getActualHeight(){
                    return Math.max(
                        Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                        Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                        Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                    );
                }
                return getActualHeight()
            """)
        driver.execute_script(
            f"window.scrollTo(0,{prev_h + 300})")  # I think it should 0. The original code is {prev_h}
        if nScroll%10 == 0:
            print("scrolled time:" + str(nScroll))
        nScroll += 1
        time.sleep(1)  # for loading data
        prev_h += 300
        if prev_h >= height:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # scrip the comment
    comment_div = soup.select('#content #content-text')
    comment_list = [x.text for x in comment_div]
    print('---- Scarped ' + str(len(comment_list)) + ' comments')
    store_data(comment_list, comment_file)
    print('---- comments stored in txt file')
