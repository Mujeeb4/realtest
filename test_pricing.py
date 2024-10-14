import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class TestPricing():
    def setup_method(self, method):
        # Set up Chrome options for headless execution (suitable for GitHub Actions)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1296, 696)

        # Create a folder for screenshots if it doesn't exist
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def teardown_method(self, method):
        self.driver.quit()

    def test_11Plus(self):
        # Navigate to the main page
        self.driver.get("https://smoothmaths.co.uk/")

        # Hover over the "Pricing" dropdown to reveal the links
        dropdown = self.driver.find_element(By.LINK_TEXT, "Pricing")
        ActionChains(self.driver).move_to_element(dropdown).perform()
        time.sleep(1)  # Adding a small pause to ensure the dropdown is fully revealed

        # Click on "11 Plus Independent Schools"
        independent_link = self.driver.find_element(By.LINK_TEXT, "Student Pricing")
        independent_link.click()
        
        # Wait for the new page to load and check the URL
        WebDriverWait(self.driver, 10).until(EC.url_contains("https://smoothmaths.co.uk/pricing/"))
        current_url = self.driver.current_url
        self.save_screenshot("pricing_page")

        if current_url == "https://smoothmaths.co.uk/pricing/":
            print("Student Pricing page link is correct")
        else:
            print(f"Error: Expected 'https://smoothmaths.co.uk/pricing/', but got {current_url}")
        
        # Navigate back to the main page to click the next link
        self.driver.get("https://smoothmaths.co.uk/")
        dropdown = self.driver.find_element(By.LINK_TEXT, "Pricing")
        ActionChains(self.driver).move_to_element(dropdown).perform()
        time.sleep(1)

        # Click on "11 Plus Grammar Schools"
        grammar_link = self.driver.find_element(By.LINK_TEXT, "Schools and Tutoring Centre Pricing")
        grammar_link.click()

        # Wait for the new page to load and check the URL
        WebDriverWait(self.driver, 10).until(EC.url_contains("https://smoothmaths.co.uk/business-packages/"))
        current_url = self.driver.current_url
        self.save_screenshot("business_pricing_page")

        if current_url == "https://smoothmaths.co.uk/business-packages/":
            print("Schools and Tutoring Centre Pricing link is correct")
        else:
            print(f"Error: Expected 'https://smoothmaths.co.uk/business-packages/', but got {current_url}")

    def save_screenshot(self, name):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = f"screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(screenshot_path)