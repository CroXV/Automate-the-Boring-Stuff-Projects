from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


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
            print('Game Over!')
            time.sleep(3)
            browser.quit()
            break


def game_over(browser):
    try:
        browser.find_element_by_class_name('game-over')
        return True
    except NoSuchElementException:
        return False


if __name__ == '__main__':
    play_game()