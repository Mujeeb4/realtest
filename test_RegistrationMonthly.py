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

class TestMonthlyPlan():
    def setup_method(self, method):
        # Use headless Chrome for CI
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1382, 744)

        # Ensure screenshots directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def teardown_method(self, method):
        self.driver.quit()

    def test_monthly_plan(self):
        start_time = time.time()

        try:
            # Navigate to the main page
            self.driver.get("https://smoothmaths.co.uk/")
            
            # Click on the "Join Now" button in the header
            join_now_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Join Now"))
            )
            join_now_button.click()

            # Scroll down to the first "Register" button for the plan
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".et_pb_pricing_table_button a"))
            )
            self.driver.execute_script("window.scrollBy(0, 400);")  # Adjust the scroll amount as needed
            time.sleep(1)

            # Click the first "Register" button
            first_register_button = self.driver.find_element(By.CSS_SELECTOR, ".et_pb_pricing_table_button a")
            first_register_button.click()

            # Wait for the page to load
            WebDriverWait(self.driver, 30).until(
                EC.url_contains("register")
            )

            # If-else block to check for correct redirection
            if "register/11-plus-subscription-plan" in self.driver.current_url:
                status = "Passed"
            else:
                status = "Failed"

            # Take a screenshot
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/{status}_monthly_plan_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)

            # Record the test result
            self._store_test_results("Test Monthly Plan", status, screenshot_path)

        except Exception as e:
            # Save a screenshot and record the test as failed if any exception occurs
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/failed_monthly_plan_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            self._store_test_results("Test Monthly Plan", "Failed", screenshot_path)
            raise AssertionError(f"Test failed: {e}")

        # Record end time and calculate duration
        end_time = time.time()
        duration = end_time - start_time
        print(f"Test duration: {round(duration, 2)} seconds")

    def _store_test_results(self, test_case, status, screenshot_path):
        # Prepare results for CSV
        results = {
            "Test Case": [test_case],
            "Status": [status],
            "Screenshot": [screenshot_path]
        }

        # Append results to the CSV file
        df = pd.DataFrame(results)
        if not os.path.exists(CSV_FILE_PATH):
            df.to_csv(CSV_FILE_PATH, index=False)
        else:
            df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)

