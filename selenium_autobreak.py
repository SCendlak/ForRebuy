from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


class SeleniumAutoBreak:
    def __init__(self, inewi_url, livefruit_url):
        self.inewi_url = inewi_url
        self.livefruit_url = livefruit_url


    def chrome_setup(self):
        chrome_options = ChromeOptions()
        profile_settings = "profile.default_content_setting_values."
        prefs = {profile_settings + "media_stream_mic": 2,
                 profile_settings + "media_stream_camera": 2,
                 profile_settings + "geolocation": 1,
                 profile_settings + "notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = Chrome(chrome_options=chrome_options)
        return driver

    def inewi_break_automation(self, inewi_email, inewi_password):
        driver = self.chrome_setup()
        driver.get(self.inewi_url)
        wait = WebDriverWait(driver, 5)
        driver.implicitly_wait(50)
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
        # driver.find_element(By.ID, "setStatusBtn").click()


    def livefruit_break_automation(self, livefruit_email, livefruit_password):
        driver = self.chrome_setup()
        driver.get(self.livefruit_url)
        driver.find_element(By.NAME, "username").send_keys(livefruit_email)
        driver.find_element(By.NAME, "password").send_keys(livefruit_password)
        driver.find_element(By.CSS_SELECTOR, ".btn")
        Select(driver.find_element(By.ID, "id_mpk")).select_by_visible_text("Przerwa")
        driver.find_element(By.CSS_SELECTOR, ".btn")


    def inewi_livefruit_break_automatization(self, inewi_email, inewi_password, livefruit_email, livefruit_password):
        self.inewi_break_automation(inewi_email, inewi_password)
        self.livefruit_break_automation(livefruit_email, livefruit_password)

