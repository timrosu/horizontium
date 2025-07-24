from time import sleep

# selenium browser driver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# selenium commands
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


def wait_for_page_to_load() -> None:
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def load_config(filename: str) -> dict:
    """Load config from text file to dictionary. Originaly meant for http headers."""
    configuration = {}
    with open(filename, "r") as f:
        for line in f:
            if not line.strip() or ":" not in line:
                continue
            key, value = line.split(":", 1)
            configuration[key.strip()] = value.strip()
    return configuration


###### CONFIG ######
config = load_config("conf/horizont.conf")
url = load_config("conf/urls.conf")
####################


# initialize web driver
options = Options()
options.add_argument("--headless")  # Remove this line if you want to see the browser
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)


# open login page
driver.get(url.get("prijava"))

## scroll to the bottom
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

## wait for creds input field to be visible
wait = WebDriverWait(driver, 10, 0.5)
username_input = wait.until(EC.presence_of_element_located((By.ID, "username_login")))
password_input = driver.find_element(By.ID, "password_login")

## enter credentials
wait_for_page_to_load()
username_input.clear()
username_input.send_keys(config.get("username"))
password_input.clear()
password_input.send_keys(config.get("password"))

## accept terms and conditions
sleep(0.5)
driver.find_element(By.ID, "strinjam_se_s_pogoji").click()

## find and click the login button
sleep(0.5)
driver.find_element(By.CSS_SELECTOR, "button.login").click()


# wait for page to load
wait_for_page_to_load()
# wait for the customer name div to appear
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#expandDisplayName"))
)


# open settings page
driver.get(url.get("telefonija"))

## select a desired phone number
number_dropdown = wait.until(EC.presence_of_element_located((By.ID, "number_selector")))
Select(number_dropdown).select_by_value(config.get("t2_number"))

## open Preusmeritve tab
number_dropdown = wait.until(
    EC.presence_of_element_located((By.LINK_TEXT, "Preusmeritve"))
).click()

## read existent unconditional redirect boolean-like entity and enable it
redirect_toggle = Select(driver.find_element(By.NAME, "CFU_menu"))

print(
    "old selected index:",
    redirect_toggle.options.index(redirect_toggle.first_selected_option),
)
if redirect_toggle != "A":
    redirect_toggle.select_by_index(0)
    sleep(0.5)
    print(
        "new selected index:",
        redirect_toggle.options.index(redirect_toggle.first_selected_option),
    )

## read existent unconditional redirect number
redirect_number = driver.find_element(By.NAME, "CFU_c_number")
old_value = redirect_number.get_attribute("value")
print("old number:", old_value)

if old_value != config.get("redirect_number"):
    print("red-num different than in conf, setting user preferred")
    redirect_number.clear()
    redirect_number.send_keys(config.get("redirect_number"))
    print("old number:", redirect_number.get_attribute("value"))
    ## save changes
    driver.find_element(By.NAME, "shrani").click()

print("✅")
driver.close()
