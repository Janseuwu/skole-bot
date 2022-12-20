from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv
import os
from prettify_schedule import *


def get_schedule(target):
    f = open('schedule.txt', 'w')

    # set options headless
    options = Options()
    options.binary_location = "/usr/bin/firefox"
    options.headless = True

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

    searchBar = driver.find_element(By.ID, 'SearchText')
    searchBar.clear()
    searchBar.send_keys(target)  
    li = driver.find_elements(By.XPATH, "//ul[contains(@id, 'SearchAutoCompleteExtender_completionListElem')]/li") 
    li[0].click()

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
