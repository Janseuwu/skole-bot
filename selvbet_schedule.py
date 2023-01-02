from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv
import os
from prettify_schedule import *
import time


def get_schedule(targetClass, targetWeek):
    f = open('schedule.txt', 'w')

    # set options headless
    options = Options()
    options.binary_location = "/usr/bin/firefox"
    options.headless = False

    # firefox driver
    driver = webdriver.Firefox(options=options, executable_path="/home/janseuwu/Documents/geckodriver") # laptop path
    # driver = webdriver.Firefox(options=options, executable_path=r"C:\Users\jaxzi\Documents\geckodriver.exe") # desktop path
    driver.implicitly_wait(10)
    driver.get("https://selvbetjening.aarhustech.dk/WebTimeTable/default.aspx")


    # login
    load_dotenv(".env")
    username = os.getenv("SECRET_NAME")
    password = os.getenv("SECRET_KEY")
    username_field = driver.find_element(By.ID, 'userNameInput')
    password_field = driver.find_element(By.ID, 'passwordInput')
    login_button = driver.find_element(By.ID, 'submitButton')
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    # specify class 
    searchBar = driver.find_element(By.ID, 'SearchText')
    searchBar.clear()
    searchBar.send_keys(targetClass)  
    li = driver.find_elements(By.XPATH, "//ul[contains(@id, 'SearchAutoCompleteExtender_completionListElem')]/li") 
    li[0].click()

    # specify week
    elem = driver.find_element(By.ID, "PeriodText")
    s = elem.text
    s = s[-2:]
    s = s.replace(" ", "")
    currentWeek = int(s)
    clickAmount = int(targetWeek) - currentWeek
    for r in range(clickAmount):
        nextWeek = driver.find_element(By.ID, "PeriodNextButton")
        nextWeek.click()
        time.sleep(0.5)

    # fetch the schedule
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for day in range(0,5):
        f.write(f"\n\n**{days[day]}**\n")
        
        id = f'day{day}Col'
        elements = driver.find_elements(By.ID, id)

        for element in elements:
            f.write(element.text) # write it to file for the discord bot to send messages from
    f.close()


    driver.close()
    prettify_schedule()
