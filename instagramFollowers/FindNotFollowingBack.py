from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

username = ''
password = ''

def scroll(driver, modal):
    # Scroll through the followers modal
    last_height = driver.execute_script("return arguments[0].scrollTop", modal)

    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;", modal)
        time.sleep(2)  # Adjust sleep time based on your internet speed

        new_height = driver.execute_script("return arguments[0].scrollTop", modal)
        if new_height == last_height:  # Break the loop if there's no new content
            break
        last_height = new_height

def click_button_with_css(driver, css_selector):
    element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    element.click()

def login(driver):
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(u'\ue007')
def to_followers(driver):
    profile_css = "[href*=\"" + username + "\"]"
    click_button_with_css(driver, profile_css)

def __main__():
    driver = webdriver.Chrome()
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(1)
    login(driver)
    to_followers(driver)

    followers_css = "[href*=\"" + username + "/followers/\"]"
    css_select_close = '[aria-label="Close"]'
    following_css = "[href*=\"" + username + "/following/\"]"

    click_button_with_css(driver, followers_css)
    time.sleep(3)
    modal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6')]"))
    )
    scroll(driver, modal)
    time.sleep(3)
    # Extract all username spans
    follower_elements = driver.find_elements(By.CSS_SELECTOR, "span._ap3a._aaco._aacw._aacx._aad7._aade")

    # Get the text of each span (the usernames)
    followers = [user.text for user in follower_elements if user.text != ""]

    click_button_with_css(driver, css_select_close)
    time.sleep(1)

    click_button_with_css(driver, following_css)
    time.sleep(3)

    modal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6')]"))
    )
    scroll(driver, modal)
    # Extract all username spans
    following_elements = driver.find_elements(By.CSS_SELECTOR, "span._ap3a._aaco._aacw._aacx._aad7._aade")

    # Get the text of each span (the usernames)
    following = [user.text for user in following_elements if user.text != ""]

    not_following_back = list(set(following) - set(followers))

    print(followers)
    print(following)
    print(not_following_back)
    return

__main__()