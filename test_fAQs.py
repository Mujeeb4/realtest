import pytest
import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

CSV_FILE_PATH = "test_results_faqs.csv"

class TestFAQs:
    def setup_method(self, method):
        # Setup headless mode for CI environments
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_fAQs(self):
        result_data = {"test_name": "test_fAQs", "status": "", "error": ""}
        try:
            # Navigate to the homepage
            self.driver.get("https://smoothmaths.co.uk/")
            self.driver.set_window_size(1296, 696)

            # Scroll down to the FAQ link in the footer and click it
            self.driver.execute_script("window.scrollTo(0, 4370.66650390625)")
            faq_link = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "FAQs"))
            )
            faq_link.click()

            # Validate the current URL to check if the link works
            WebDriverWait(self.driver, 20).until(EC.url_contains("faqs"))
            current_url = self.driver.current_url
            assert current_url == "https://smoothmaths.co.uk/faqs/", f"Unexpected URL: {current_url}"

            # Test each FAQ toggle, ensuring all expand and collapse
            faq_items = [
                ".et_pb_accordion_item_1 > .et_pb_toggle_title",
                ".et_pb_accordion_item_2 > .et_pb_toggle_title",
                ".et_pb_accordion_item_3 > .et_pb_toggle_title",
                ".et_pb_accordion_item_4 > .et_pb_toggle_title",
                ".et_pb_accordion_item_5 > .et_pb_toggle_title",
                ".et_pb_accordion_item_6 > .et_pb_toggle_title"
            ]
            
            for faq in faq_items:
                faq_element = WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, faq))
                )
                faq_element.click()
                # Use WebDriverWait instead of sleep to wait for the element to change state
                WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, faq))
                )

            # Take a screenshot after all FAQs have been clicked
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/faqs_test_{timestamp}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            self.driver.save_screenshot(screenshot_path)

            # Assert the screenshot is saved successfully
            assert os.path.exists(screenshot_path), "Screenshot not saved!"
            result_data["status"] = "Passed"
        except Exception as e:
            result_data["status"] = "Failed"
            result_data["error"] = str(e)
            # Capture the error screenshot
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            error_screenshot_path = f"screenshots/faqs_error_{timestamp}.png"
            self.driver.save_screenshot(error_screenshot_path)

        # Save the results in a CSV file
        self.save_results_to_csv(result_data)

    def save_results_to_csv(self, result_data):
        file_exists = os.path.isfile(CSV_FILE_PATH)
        with open(CSV_FILE_PATH, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["test_name", "status", "error"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(result_data)
