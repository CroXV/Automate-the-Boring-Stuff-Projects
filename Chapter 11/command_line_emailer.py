#! /usr/bin/env python
# Usage: py.exe command_line_emailer.py <botmail> <botpass>

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import re
import time
import sys
import base64
import json


def open_browser():
    # Get bot info
    bot_email, botpass = bot_info()
    # Gets reciever's information
    email = rec_email()
    subj, msg = sending_msg()

    # Opens firefox with selenium
    browser = webdriver.Firefox()
    browser.minimize_window()
    browser.get('https://mail.google.com')
    browser.implicitly_wait(5)

    # Logs into bot's email
    open_bot_mail(browser, bot_email, botpass)
    compose_message(browser, email, subj, msg)

    # waits until message is sent before exiting browser
    time.sleep(5)
    browser.quit()
    print('Message was sent successfully!')


def open_bot_mail(browser, bot_email, botpass):
    # Enter email address
    email = browser.find_element_by_name('identifier')
    email.send_keys(bot_email)
    email.send_keys(Keys.ENTER)

    # Enter password
    add_delay(browser, By.CSS_SELECTOR, 'input[type="password"]')
    password = browser.find_element_by_css_selector('input[type="password"]')
    password.send_keys(botpass)
    password.send_keys(Keys.ENTER)


def compose_message(browser, email, rec_subject, rec_message):
    # Clicks compose message
    add_delay(browser, By.CSS_SELECTOR, 'div.z0 div')
    browser.find_element_by_css_selector('div.z0 div').click()

    # Enters reciever's email
    add_delay(browser, By.CSS_SELECTOR, 'textarea.vO')
    send_to = browser.find_element_by_css_selector('textarea.vO')
    send_to.send_keys(email)

    # Enters subject
    add_delay(browser, By.CSS_SELECTOR, 'input.aoT')
    subject = browser.find_element_by_css_selector('input.aoT')
    subject.send_keys(rec_subject)

    # Enters message
    add_delay(browser, By.CSS_SELECTOR, 'div.LW-avf')
    message = browser.find_element_by_css_selector('div.LW-avf')
    message.send_keys(rec_message)

    # Sends message
    browser.find_element_by_css_selector('div.v7').click()


def bot_info():
    saved = load_botinfo()
    if len(sys.argv) == 3:
        bot_email = sys.argv[1]
        botpass = sys.argv[2]

        if parse_email(bot_email):
            save_botinfo(bot_email, botpass)
            return bot_email, botpass
        else:
            raise Exception('Invalid email address.')
    elif saved:
        return saved
    else:
        raise Exception('Not enough arguments.')


def save_botinfo(bot_email, botpass):
    data = {'email': bot_email, 'password': encode_pass(botpass)}
    with open('botinfo.json', 'w') as f:
        json.dump(data, f)


def load_botinfo():
    try:
        with open('botinfo.json') as f:
            data = json.load(f)
            bot_email = data['email']
            botpass = decode_pass(data['password'])

            return bot_email, botpass
    except FileNotFoundError:
        pass


def rec_email():
    print('(Press Q to exit.)')
    print('Enter reciever\'s email address:')
    while True:
        email = input('> ')
        if email.lower() == 'q':
            sys.exit()
        elif parse_email(email):
            return email
        else:
            print('Re-enter: Incorrect email address.')


def sending_msg():
    subj = input('Enter subject.\n> ')
    if subj.lower() == 'q':
        sys.exit()

    msg = input('Enter Message.\n> ')
    if msg.lower() == 'q':
        sys.exit()

    print('\nSending Message...')
    return subj, msg


def parse_email(email):
    email_check = re.compile(r'^\w[a-zA-Z0-9._-]+@\w[a-zA-Z0-9._-]+\.\w{2,4}$')
    return email_check.search(email)


def encode_pass(password):
    # turn password into bytes
    byte = password.encode('utf-8')
    # store base 64 encoding in a list for json
    enc = list(base64.b64encode(byte))

    return enc


def decode_pass(password):
    enc_pass = ''.join(chr(b) for b in password).encode('utf-8')
    dec_pass = base64.b64decode(enc_pass)
    str_pass = str(dec_pass, 'utf-8')

    return str_pass


def add_delay(browser, attribute, value, wait=20, delay=2):
    try:
        # Checks if page loads before wait timer
        WebDriverWait(browser, wait).until(
            ec.presence_of_element_located((attribute, value)))
        # Waits after page loads
        time.sleep(delay)
    except Exception as err:
        print(f'Page did not load in time.\n{err}')
        sys.exit()


if __name__ == '__main__':
    open_browser()
