import pytest
import time
import os
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CSV file path to store test results
CSV_FILE_PATH = "test_results.csv"

class TestTermsConditions():
    def setup_method(self, method):
        # Use headless Chrome for CI
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.vars = {}
  
    def teardown_method(self, method):
        self.driver.quit()
  
    def test_termsConditions(self):
        start_time = time.time()

        # Navigate to the main page
        self.driver.get("https://smoothmaths.co.uk/")
        self.driver.set_window_size(1296, 696)

        # Scroll down to make the Terms & Conditions link visible
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Explicitly wait for the element to be clickable
        try:
            terms_link = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a:nth-child(3) > span"))
            )
            terms_link.click()
        except Exception as e:
            raise AssertionError(f"Could not interact with the Terms & Conditions link. Error: {e}")

        # Check if the browser navigated to the correct URL
        try:
            WebDriverWait(self.driver, 10).until(EC.url_to_be("https://smoothmaths.co.uk/terms-conditions/"))

            # Save screenshot with timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/terms_conditions_{timestamp}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            self.driver.save_screenshot(screenshot_path)

            # Store test result in CSV
            self._store_test_results("Test Terms & Conditions", "Passed", screenshot_path)

        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            self._store_test_results("Test Terms & Conditions", "Failed", "No screenshot - test failed")
            raise AssertionError(f"Terms & Conditions test failed. Error: {e}")

    def _store_test_results(self, test_case, status, screenshot_path):
        # Save test results in a CSV file
        results = {
            "Test Case": [test_case],
            "Status": [status],
            "Screenshot": [screenshot_path]
        }
        df = pd.DataFrame(results)
        if not os.path.exists(CSV_FILE_PATH):
            df.to_csv(CSV_FILE_PATH, index=False)
        else:
            df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)

