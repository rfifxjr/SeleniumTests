import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class TestWebApp:
    @pytest.fixture(scope="class")
    def setup(self):
        # Установка ChromeDriver с помощью webdriver-manager
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://the-internet.herokuapp.com/")
        yield
        self.driver.quit()

    def test_login_success(self, setup):
        self.driver.find_element(By.LINK_TEXT, "Form Authentication").click()
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)  # Ожидание загрузки страницы
        assert "Secure Area" in self.driver.title

    def test_login_failure(self, setup):
        self.driver.find_element(By.LINK_TEXT, "Form Authentication").click()
        self.driver.find_element(By.ID, "username").send_keys("wrongusername")
        self.driver.find_element(By.ID, "password").send_keys("wrongpassword")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)  # Ожидание загрузки страницы
        error_message = self.driver.find_element(By.ID, "flash").text
        assert "Your username is invalid!" in error_message
