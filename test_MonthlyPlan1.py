import pytest
import time
import os
import datetime
import pandas as pd  # <--- Add this import for pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CSV file path to store test results
CSV_FILE_PATH = "test_results.csv"

class TestPlan1():
    def setup_method(self, method):
        # Use headless Chrome for CI
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1920, 1080)  # Adjust screen size for better screenshots

        # Ensure screenshots directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def teardown_method(self, method):
        self.driver.quit()

    def test_plan_1(self):
        start_time = time.time()
        pricing_page = "https://smoothmaths.co.uk/pricing/"
        expected_url = "https://smoothmaths.co.uk/register/11-plus-subscription-plan/"

        try:
            # Navigate directly to the pricing page
            self.driver.get(pricing_page)
            print("Navigating to the pricing page for Plan 1")

            # Wait for the page to load and verify we're on the pricing page
            WebDriverWait(self.driver, 60).until(
                EC.url_to_be(pricing_page)
            )
            print("Successfully navigated to pricing page")

            # Locate the "Register" button for Plan 1 and click it
            register_button = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Register')]"))
            )

            # Scroll into view and click the button
            self.driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", register_button)

            # Wait for the redirection to the registration page
            print(f"Waiting for redirection to {expected_url}")
            WebDriverWait(self.driver, 120).until(
                EC.url_contains(expected_url)
            )

            # Check if we were redirected to the expected checkout/payment page
            current_url = self.driver.current_url
            if current_url == expected_url:
                print("Successfully navigated to the expected URL")
                status = "Passed"
            else:
                print(f"Unexpected URL: {current_url}")
                status = "Failed"

            # Take a screenshot of the checkout/payment page
            time.sleep(2)  # Pause to allow the page to load fully
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/plan_1_{status}_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)

            # Record the test result
            self._store_test_results("Plan 1 Registration", status, screenshot_path)

        except Exception as e:
            # Log the exception and save a failure screenshot
            print(f"Exception occurred: {str(e)}")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/plan_1_failed_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            self._store_test_results("Plan 1 Registration", "Failed", screenshot_path)

        finally:
            # Record end time and calculate duration
            end_time = time.time()
            duration = end_time - start_time
            print(f"Test duration for Plan 1: {round(duration, 2)} seconds")

    def _store_test_results(self, test_case, status, screenshot_path):
        # Prepare results for CSV
        results = {
            "Test Case": [test_case],
            "Status": [status],
            "Screenshot": [screenshot_path]
        }

        # Append results to the CSV file
        if not os.path.exists(CSV_FILE_PATH):
            pd.DataFrame(results).to_csv(CSV_FILE_PATH, index=False)
        else:
            pd.DataFrame(results).to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
