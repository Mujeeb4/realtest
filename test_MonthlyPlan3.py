import pytest
import time
import os
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, WebDriverException

# CSV file path to store test results
CSV_FILE_PATH = "test_results.csv"

class TestPlan2():
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

    def click_with_retry(self, locator, retries=3):
        """Clicks an element with retry mechanism"""
        attempts = 0
        while attempts < retries:
            try:
                element = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located(locator)
                )
                # Scroll the element into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                # Use JavaScript to ensure it's clickable
                self.driver.execute_script("arguments[0].click();", element)
                print(f"Element clicked successfully on attempt {attempts + 1}")
                return True
            except (TimeoutException, ElementClickInterceptedException, WebDriverException) as e:
                print(f"Failed to click element on attempt {attempts + 1}: {e}")
                attempts += 1
                time.sleep(2)  # Wait before retrying
        print(f"Failed to click element after {retries} retries.")
        return False

    def test_plan_2(self):
        start_time = time.time()
        pricing_page = "https://smoothmaths.co.uk/pricing/"
        expected_url = "https://smoothmaths.co.uk/register/13-plus-subscription-plan/"

        try:
            # Navigate directly to the pricing page
            self.driver.get(pricing_page)
            print("Navigating to the pricing page for Plan 3")

            # Wait for the page to load and verify we're on the pricing page
            WebDriverWait(self.driver, 60).until(EC.url_to_be(pricing_page))
            print("Successfully navigated to pricing page")

            
            # Locate and click the "Register" button for the second yearly plan (Plan 2)
            register_locator = (By.XPATH, "(//a[contains(text(), 'Register')])[3]")
            if not self.click_with_retry(register_locator):
                raise Exception("Failed to click the Register button for Plan 3 after retries.")

            # Log the current URL for debugging purposes
            print(f"Current URL after clicking the register button: {self.driver.current_url}")

            # Wait for the redirection to the registration page
            print(f"Waiting for redirection to {expected_url}")
            WebDriverWait(self.driver, 120).until(EC.url_contains(expected_url))

            # Check if we were redirected to the expected checkout/payment page
            current_url = self.driver.current_url
            print(f"Expected URL: {expected_url}, Current URL: {current_url}")
            if current_url == expected_url:
                print("Successfully navigated to the expected URL")
                status = "Passed"
            else:
                print(f"Unexpected URL: {current_url}")
                status = "Failed"

            # Take a screenshot of the checkout/payment page
            time.sleep(2)  # Pause to allow the page to load fully
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/Monthly_plan_3_{status}_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)

            # Record the test result
            self._store_test_results("Monthly Plan 3 Registration", status, screenshot_path)

        except Exception as e:
            # Log the exception and save a failure screenshot
            print(f"Exception occurred: {str(e)}")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/Monthly_plan_3_failed_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            self._store_test_results("Monthly Plan 3 Registration", "Failed", screenshot_path)

        finally:
            # Record end time and calculate duration
            end_time = time.time()
            duration = end_time - start_time
            print(f"Test duration for Plan 3: {round(duration, 2)} seconds")

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
