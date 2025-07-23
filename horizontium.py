from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located


# initialize web driver
options = Options()
# options.add_argument("--headless")  # Remove this line if you want to see the browser
driver = webdriver.Firefox(options=options)
base_url="https://horizont.t-2.net"


###### CONFIG ######
conf_t2_number = [redacted]
conf_redirect_number = [redacted]
####################


# open login page
driver.get(f"{base_url}/prijava")

## wait for creds input field to be visible
wait = WebDriverWait(driver, 10)
username_input = wait.until(EC.presence_of_element_located((By.ID, "username_login")))
password_input = driver.find_element(By.NAME, "password_login")

## enter credentials
username_input.send_keys("[redacted]")
password_input.send_keys("[redacted]")

## accept terms and conditions
driver.find_element(By.ID, "strinjam_se_s_pogoji").click()

## find and click the login button
driver.find_element(By.CSS_SELECTOR, ".primary").click()


# open settings page
driver.get(f"{base_url}/nastavitve/telefonija")

## select a desired phone number
number_dropdown = driver.find_element(By.ID, "number_selector")
Select(number_dropdown).select_by_value(f"label={conf_t2_number}")

## open Preusmeritve tab
driver.find_element(By.LINK_TEXT, "Preusmeritve").click()

## read existent unconditional redirect boolean-like entity and enable it
redirect_enabled_menu = driver.find_element(By.NAME, "CFU_c_menu")
if redirect_enabled_menu is "Ne":
   Select(redirect_enabled_menu).select_by_value(f"Da")

## read existent unconditional redirect number
redirect_number = driver.find_element(By.NAME, "CFU_c_number")
if redirect_number is not conf_redirect_number:
   redirect_number.send_keys(conf_redirect_number)

## save changes
driver.find_element(By.NAME, "shrani").click()
