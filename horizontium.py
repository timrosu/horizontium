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
config = load_config("conf/horizontium.conf")
url = load_config("conf/urls.conf")
####################


# initialize web driver
options = Options()
options.add_argument("--headless")  # Remove this line if you want to see the browser
print("installing geckodriver")
service = Service(GeckoDriverManager().install())
print("installed geckodriver")
driver = webdriver.Firefox(service=service, options=options)
driver.set_window_size(1936, 1048)


# open settings page (redirects to login)
driver.get(url.get("telefonija"))

## wait for redirection to login page
wait_for_page_to_load()

## find fields
username_input = driver.find_element(By.NAME, "email")
password_input = driver.find_element(By.ID, "password")

## enter creds
username_input.clear()
username_input.send_keys(config.get("username"))
print("🤓👉 entered username")
password_input.clear()
password_input.send_keys(config.get("password"))
print("🤓👉 entered password")

## find and click the login button
sleep(0.5)
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#submitButton"))
).click()

# locate otp input field
otp_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#sms-token"))
)
otp_input.clear()

otp_token=input("💬 Enter OTP code: ")
otp_input.send_keys(otp_token)
print("🤓👉 submitted OTP code")

## find and click the login button
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#submitButton"))
).click()
print("🤓👉 logged in")

wait_for_page_to_load()

## accept cookies (cause why th not)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#cookieBtnIzberiObvezne > span:nth-child(1)"))
).click()
print("🤓👉 accepted cookies 🍪🍪🍪")

## open redirection tab
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#tab-t4"))
).click()
print("🤓👉 selected redirection tab")

## wait for number input field
redirect_number = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='stevilka-input el-input'] input[placeholder='Vpišite številko (npr. +38664064064)']"))
)
print("🤓👉 found number input field")

## read currently set unconditional redirect number
old_red_num = redirect_number.get_attribute("value")
print("️️📞 old number:", old_red_num)

if old_red_num != config.get("redirect_number"):
    print("️️📞 number different than in conf, setting user preferred")
    redirect_number.clear()
    print("🤓👉 cleared old number")
    redirect_number.send_keys(config.get("redirect_number"))
    print("🤓👉 typed in your number")
    print("️️📞 new number:", redirect_number.get_attribute("value"))
    ## save changes
    driver.find_element(By.CSS_SELECTOR, ".shrani-gumb > span").click()
    print("🤓👉 saved changes")

print("✅")

# logout
driver.find_element(By.ID, "t2logoutbtn").click()
print("🤓👉 logged out") #TODO: make verbosity optional with debug option in config
driver.close()
