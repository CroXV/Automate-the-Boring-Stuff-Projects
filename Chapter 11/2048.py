#! /usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import re


def play_game():
    browser = webdriver.Firefox()
    browser.get('https://gabrielecirulli.github.io/2048/')
    page = browser.find_element_by_tag_name('html')

    while True:
        page.send_keys(Keys.UP)
        page.send_keys(Keys.RIGHT)
        page.send_keys(Keys.DOWN)
        page.send_keys(Keys.LEFT)

        if game_over(browser):
            score = browser.find_element_by_class_name('score-container')
            score = re.compile(r'\d+').search(score.text)
            print(f'Game Over! Score: {score.group()}')
            time.sleep(5)
            retry(browser)


def retry(browser):
    try:
        browser.find_element_by_class_name('retry-button').click()
    except NoSuchElementException:
        pass


def game_over(browser):
    try:
        browser.find_element_by_class_name('game-over')
        return True
    except NoSuchElementException:
        return False


if __name__ == '__main__':
    play_game()