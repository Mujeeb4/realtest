import pytest
import time
import os
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# CSV file path to store test results
CSV_FILE_PATH = "test_results.csv"

class TestSubscription():
    def setup_method(self, method):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1920, 1080)

        # Ensure screenshots directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def teardown_method(self, method):
        self.driver.quit()

    def test_subscription(self):
        start_time = time.time()
        try:
            # Navigate to subscription page
            self.driver.get("https://smoothmaths.co.uk/register/11-plus-subscription-plan/")
            print("Navigating to the subscription page")

            # Fill in the form fields
            self.driver.find_element(By.ID, "mepr-address-one").send_keys("Muslim road")
            self.driver.find_element(By.ID, "mepr-address-city").send_keys("Lahore")
            dropdown = self.driver.find_element(By.ID, "mepr-address-country")
            dropdown.find_element(By.XPATH, "//option[. = 'Pakistan']").click()
            self.driver.find_element(By.ID, "mepr_full_name1").send_keys("Hanzila Rafiq")
            self.driver.find_element(By.NAME, "mepr-address-state").send_keys("Punjab")
            self.driver.find_element(By.ID, "mepr-address-zip").send_keys("590000")
            self.driver.find_element(By.ID, "user_email1").send_keys("mujeebnawaz42@gmail.com")
            self.driver.find_element(By.ID, "mepr_user_password1").send_keys("Hanzila*183258")
            self.driver.find_element(By.ID, "mepr_user_password_confirm1").send_keys("Hanzila*183258")

            # Switch to payment iframe and fill in payment details
            self.driver.switch_to.frame(4)
            self.driver.find_element(By.ID, "Field-numberInput").send_keys("4649 5102 1304 1970")
            self.driver.find_element(By.ID, "Field-cvcInput").send_keys("885")
            self.driver.find_element(By.ID, "Field-expiryInput").send_keys("08 / 27")
            self.driver.switch_to.default_content()

            # Submit the form
            self.driver.find_element(By.CSS_SELECTOR, ".mepr-submit").click()

            # Wait for 'Thank You' text to appear
            thank_you_text = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Thank you')]"))
            )
            assert "Thank you" in thank_you_text.text
            print("Form submitted successfully, 'Thank You' message found.")

            # Take a screenshot of the checkout/payment page
            time.sleep(2)  # Pause to allow the page to load fully
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/plan_1_{status}_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)

            status = "Passed"
        
        except TimeoutException:
            # Handle the exception and save a failure screenshot
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/subscription_failed_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Exception occurred: Timed out waiting for the Thank You message.")
            status = "Failed"

        finally:
            # Save the results in a CSV file
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            self._store_test_results("Subscription Test", status, screenshot_path, duration)
            print(f"Test completed in {duration} seconds.")

    def _store_test_results(self, test_case, status, screenshot_path, duration):
        # Prepare results for CSV
        results = {
            "Test Case": [test_case],
            "Status": [status],
            "Screenshot": [screenshot_path],
            "Duration": [duration]
        }

        # Append results to the CSV file
        if not os.path.exists(CSV_FILE_PATH):
            pd.DataFrame(results).to_csv(CSV_FILE_PATH, index=False)
        else:
            pd.DataFrame(results).to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)

