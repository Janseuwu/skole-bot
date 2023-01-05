from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
from prettify_schedule import *
import time


def get_schedule(targetClass, targetWeek):
    f = open('schedule.txt', 'w')
    f.write("")
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

    # specify class 
    try:
        targetClass = targetClass.strip()
        searchBar = driver.find_element(By.ID, 'SearchText')
        searchBar.clear()
        searchBar.send_keys(targetClass)  
        if " " in targetClass:
            searchBar.send_keys(Keys.RETURN)
        else:
            li = driver.find_elements(By.XPATH, "//ul[contains(@id, 'SearchAutoCompleteExtender_completionListElem')]/li") 
            li[0].click()

    except:
        print("specify class error")
        f.write("Not a valid class/person")
        f.close()
        return

    # specify week
    elem = driver.find_element(By.ID, "PeriodText")
    s = elem.text
    s = s[-2:]
    s = s.replace(" ", "")
    currentWeek = int(s)
    targetWeek = int(targetWeek)
    clickAmount = targetWeek - currentWeek
    if targetWeek > 52 or targetWeek < currentWeek:
        f.write("Not a valid week bruh")
        f.close()
        print("specify week error")
        return
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
