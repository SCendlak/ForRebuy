from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


def inewi_livefruit_break_automatization(inewi_email, inewi_password, livefruit_email, livefruit_password):
    chrome_options = ChromeOptions()
    profile_settings = "profile.default_content_setting_values."
    prefs = {profile_settings + "media_stream_mic": 2,
             profile_settings + "media_stream_camera": 2,
             profile_settings + "geolocation": 1,
             profile_settings + "notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = Chrome(chrome_options=chrome_options)
    driver.get("https://inewi.pl/kiosk/")
    wait = WebDriverWait(driver, 5)
    driver.implicitly_wait(5)
    wait.until(EC.presence_of_element_located((By.ID, 'Email')))
    driver.find_element(By.ID, "Email").send_keys(str(inewi_email))
    driver.find_element(By.ID, "Password").send_keys(str(inewi_password))
    driver.find_element(By.ID, "btnSubmit").click()
    driver.find_element(By.ID, "UserLogin").send_keys(str(inewi_email))
    password_input = driver.find_element(By.ID, "Password")
    password_input.send_keys(str(inewi_password))
    driver.find_element(By.TAG_NAME, "button").click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "form-control")))
    select_element = driver.find_element(By.CLASS_NAME, "statusSelect")
    select_object = Select(select_element)
    select_object.select_by_visible_text("Przerwa")
    driver.find_element(By.ID, "setStatusBtn").click()
    driver.get("172.25.0.50:8000/allocation/add/")
    driver.find_element(By.NAME, "username").send_keys(livefruit_email)
    driver.find_element(By.NAME, "password").send_keys(livefruit_password)
    driver.find_element(By.CSS_SELECTOR, ".btn")
    Select(driver.find_element(By.ID, "id_mpk")).select_by_visible_text("Przerwa")
    driver.find_element(By.CSS_SELECTOR, ".btn")
