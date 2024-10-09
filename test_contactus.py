# Updated test_contactus.py

import pytest
import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestContactus:
    def setup_method(self, method):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_contactus(self):
        try:
            # Open the website
            self.driver.get("https://smoothmaths.co.uk/")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Contact us")))

            # Scroll and click the Contact us link
            self.driver.execute_script("window.scrollTo(0, 400)")
            self.driver.find_element(By.LINK_TEXT, "Contact us").click()

            # Wait for contact form fields to appear
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "et_pb_contact_name_0")))

            # Fill out the contact form
            self.driver.find_element(By.ID, "et_pb_contact_name_0").send_keys("Hanzila")
            self.driver.find_element(By.ID, "et_pb_contact_email_0").send_keys("hanzila@dovidigital.com")
            self.driver.find_element(By.ID, "et_pb_contact_message_0").send_keys("Testing")

            # Fill out Captcha and submit the form
            captcha_field = self.driver.find_element(By.NAME, "et_pb_contact_captcha_0")
            captcha_field.send_keys("19")  # Ensure captcha handling
            self.driver.find_element(By.NAME, "et_builder_submit_button").click()

            # Wait for the success message and check it
            success_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".et-pb-contact-message"))
            )

            assert "Thanks for contacting us" in success_message.text

            # Take a screenshot
            screenshot_path = os.path.join("screenshots", "contact_us_success.png")
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            self.driver.save_screenshot(screenshot_path)

            # Log result in CSV
            with open('test_results.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Contact Us Test", "Passed", time.strftime("%Y-%m-%d %H:%M:%S")])

        except Exception as e:
            # If the test fails, take a screenshot and log failure
            screenshot_path = os.path.join("screenshots", "contact_us_failure.png")
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            self.driver.save_screenshot(screenshot_path)

            with open('test_results.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Contact Us Test", "Failed", time.strftime("%Y-%m-%d %H:%M:%S"), str(e)])

            raise

