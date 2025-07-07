from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager




def login_to_portal(config):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(config["login_link"])
    driver.maximize_window()

    driver.find_element(By.ID, "username").send_keys(config["email"])
    Select(driver.find_element(By.ID, "dd")).select_by_value(config["day"] + " ")
    Select(driver.find_element(By.ID, "mm")).select_by_value(config["month"])
    Select(driver.find_element(By.ID, "yyyy")).select_by_value(config["year"])

    login_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @value="Login"]'))
    )
    driver.execute_script("arguments[0].click();", login_btn)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "id-type-select"))
    )
    Select(driver.find_element(By.ID, "id-type-select")).select_by_value(config["verification_type"])

    inputs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "digit-input"))
    )
    for i, digit in enumerate(config["last_4_digits"]):
        inputs[i].send_keys(digit)

    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @value="Submit"]'))
    )
    driver.execute_script("arguments[0].click();", submit_btn)

    return driver 
