import pytest
import time
import os
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

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
        expected_url = "https://smoothmaths.co.uk/register/11-plus-subscription-plan-yearly"

        try:
            # Navigate directly to the pricing page
            self.driver.get(pricing_page)
            print("Navigating to the pricing page for Plan 1")

            # Wait for the page to load and verify we're on the pricing page
            WebDriverWait(self.driver, 60).until(EC.url_to_be(pricing_page))
            print("Successfully navigated to pricing page")

            # Click the "Yearly" button using JavaScript and XPath
            yearly_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//button/span[contains(text(),'Yearly')]/.."))
            )
            self.driver.execute_script("arguments[0].click();", yearly_button)
            print("Yearly button clicked via JavaScript")
            
            time.sleep(2)

            # Retry mechanism for clicking the "Register" button
            for attempt in range(3):  # Retry up to 3 times
                try:
                    # Locate the "Register" button for the first yearly plan
                    register_button = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, "(//a[contains(text(), 'Register')])[1]"))
                    )

                    # Check if the button is clickable and visible
                    if register_button.is_displayed() and register_button.is_enabled():
                        # Try clicking with JavaScript
                        self.driver.execute_script("arguments[0].click();", register_button)
                        print("Register button clicked via JavaScript")
                        break
                    else:
                        raise Exception("Register button is not clickable or visible")
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(2)  # Wait before retrying

            # Log the current URL for debugging purposes
            print(f"Current URL after clicking the register button: {self.driver.current_url}")

            # Wait for the redirection to the registration page
            print(f"Waiting for redirection to {expected_url}")
            WebDriverWait(self.driver, 120).until(EC.url_contains(expected_url))

            # Check if we were redirected to the expected checkout/payment page
            current_url = self.driver.current_url
            print(f"Expected URL: {expected_url}, Current URL: {current_url}")
            status = "Passed" if current_url == expected_url else "Failed"

            # Take a screenshot of the checkout/payment page
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
