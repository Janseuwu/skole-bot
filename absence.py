from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv
import os
import time

def get_absence():
    options = Options()
    options.binary_location = "/usr/bin/firefox"
    options.headless = True # set option headless

    driver = webdriver.Firefox(options=options, executable_path="/home/janseuwu/Documents/geckodriver")
    driver.implicitly_wait(10)
    driver.get("https://selvbetjening.aarhustech.dk/ASDashboard/myabsence.aspx") 

    # login
    load_dotenv("fortnite.env")
    username = os.getenv("SECRET_NAME")
    password = os.getenv("SECRET_KEY")
    username_field = driver.find_element(By.ID, 'userNameInput')
    password_field = driver.find_element(By.ID, 'passwordInput')
    login_button = driver.find_element(By.ID, 'submitButton')
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()


    XPATH_dropdown = "/html/body/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div"
    XPATH_option = "/html/body/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div/div[2]/div[8]"
    dropdown = driver.find_element(By.XPATH, XPATH_dropdown)
    dropdown.click()
    time.sleep(1)

    interval = driver.find_element(By.XPATH, XPATH_option)
    interval.click()
    time.sleep(5)

    elements = driver.find_elements(By.CLASS_NAME, 'StudentAbsenceSingle')
    absencePercentage = ''
    for element in elements:
        absencePercentage = absencePercentage + element.text 

    absencePercentage = absencePercentage.replace(" ", "")
    absence = f"Janek's absence is at {absencePercentage}"
    return absence
