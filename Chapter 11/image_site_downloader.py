from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import re
import os
import time


def image_downloader():
    search = input('What images would you like for me to download?\n> ')
    new_dir = make_new_dir(search)

    browser = webdriver.Firefox()
    browser.minimize_window()

    browser.get(f'https://flicker.com/search/?text={search}')
    browser.find_element_by_tag_name('html').send_keys(Keys.END)

    # Wait before getting source
    time.sleep(2)
    source = browser.page_source
    browser.quit()

    find_img(source, new_dir)


def find_img(source, new_dir):
    soup = BeautifulSoup(source, 'html.parser')
    imgs = soup.find_all(class_=
                         'view photo-list-photo-view ' +
                         'requiredToShowOnServer awake')
    for img in imgs:
        url, img_name = parse_url(img['style'])
        resp = requests.get(url)
        resp.raise_for_status()

        file = os.path.join(new_dir, img_name)
        with open(file, 'wb') as img_file:
            for chunk in resp.iter_content(100000):
                img_file.write(chunk)


def make_new_dir(search):
    new_dir = os.path.join('images', search)
    os.makedirs(new_dir, exist_ok=True)
    return new_dir


def parse_url(img):
    check = re.compile(r'live.staticflickr.com/\d+/(.+\.\w{3})').search(img)
    url = f'https://{check.group()}'
    img_name = check.group(1)

    return url, img_name


if __name__ == '__main__':
    image_downloader()