import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Test11Plus():
    def setup_method(self, method):
    
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1296, 696)

        
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def teardown_method(self, method):
        self.driver.quit()

    def test_11Plus(self):
        # Navigate to the main page
        self.driver.get("https://smoothmaths.co.uk/")

        # Hover over the "11 Plus" dropdown to reveal the links
        dropdown = self.driver.find_element(By.LINK_TEXT, "11 Plus")
        ActionChains(self.driver).move_to_element(dropdown).perform()
        time.sleep(1)

        
        independent_link = self.driver.find_element(By.LINK_TEXT, "11 Plus Independent Schools")
        independent_link.click()
        
        # Wait for the new page to load and check the URL
        WebDriverWait(self.driver, 10).until(EC.url_contains("11-plus-schools"))
        current_url = self.driver.current_url
        self.save_screenshot("independent_schools_page")

        if current_url == "https://smoothmaths.co.uk/11-plus-schools/":
            print("11 Plus Independent Schools link is correct")
        else:
            print(f"Error: Expected 'https://smoothmaths.co.uk/11-plus-schools/', but got {current_url}")
        
        # Navigate back to the main page to click the next link
        self.driver.get("https://smoothmaths.co.uk/")
        dropdown = self.driver.find_element(By.LINK_TEXT, "11 Plus")
        ActionChains(self.driver).move_to_element(dropdown).perform()
        time.sleep(1)

        # Click on "11 Plus Grammar Schools"
        grammar_link = self.driver.find_element(By.LINK_TEXT, "11 Plus Grammar Schools")
        grammar_link.click()

        # Wait for the new page to load and check the URL
        WebDriverWait(self.driver, 10).until(EC.url_contains("11-plus-grammar-schools"))
        current_url = self.driver.current_url
        self.save_screenshot("grammar_schools_page")

        if current_url == "https://smoothmaths.co.uk/11-plus-grammar-schools/":
            print("11 Plus Grammar Schools link is correct")
        else:
            print(f"Error: Expected 'https://smoothmaths.co.uk/11-plus-grammar-schools/', but got {current_url}")

    def save_screenshot(self, name):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = f"screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(screenshot_path)

