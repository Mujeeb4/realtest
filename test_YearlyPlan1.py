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

class TestPlanYearly():
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

    def test_plan_yearly(self):
        start_time = time.time()
        pricing_page = "https://smoothmaths.co.uk/pricing/"
        
        try:
            # Navigate directly to the pricing page
            self.driver.get(pricing_page)
            print("Navigating to the pricing page for Yearly Plans")

            # Wait for the page to load and verify we're on the pricing page
            WebDriverWait(self.driver, 60).until(
                EC.url_to_be(pricing_page)
            )
            print("Successfully navigated to pricing page")

            # Locate the "Yearly Plan" button by class and click it
            yearly_plan_button = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, "df-cs-button.secondary.df-cs-icon-left"))
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", yearly_plan_button)
            time.sleep(1)
            yearly_plan_button.click()
            print("Yearly plan button clicked")

            # Define the register button classes for the yearly plans
            register_button_classes = [
                "et_pb_button df_6709694ca8586_et_pb_button_5 et_pb_bg_layout_light",
                "et_pb_button df_6709694ca8586_et_pb_button_6 et_pb_bg_layout_light",
                "et_pb_button df_6709694ca8586_et_pb_button_7 et_pb_bg_layout_light",
                "et_pb_button df_6709694ca8586_et_pb_button_8 et_pb_bg_layout_light",
                "et_pb_button df_6709694ca8586_et_pb_button_9 et_pb_bg_layout_light"
            ]

            # Loop through each register button class, click it, and take a screenshot
            for index, button_class in enumerate(register_button_classes):
                self._click_and_screenshot_button(button_class, index + 1)

        except Exception as e:
            # Log the exception and save a failure screenshot
            print(f"Exception occurred: {str(e)}")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/yearly_plan_failed_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            self._store_test_results("Yearly Plan", "Failed", screenshot_path)

        finally:
            # Record end time and calculate duration
            end_time = time.time()
            duration = end_time - start_time
            print(f"Test duration for Yearly Plan: {round(duration, 2)} seconds")

    def _click_and_screenshot_button(self, button_class, plan_number):
        try:
            # Locate the register button by class and click it
            register_button = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, button_class))
            )
            print(f"Found and clicking button for plan {plan_number}")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
            time.sleep(1)
            register_button.click()

            # Wait for the redirection and capture a screenshot
            time.sleep(3)  # Allow time for the redirection to complete
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/plan_yearly_{plan_number}_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)

            # Record the test result
            self._store_test_results(f"Yearly Plan {plan_number} Registration", "Passed", screenshot_path)

            # Navigate back to the pricing page to capture the next button
            self.driver.get("https://smoothmaths.co.uk/pricing/")
            WebDriverWait(self.driver, 60).until(
                EC.url_to_be("https://smoothmaths.co.uk/pricing/")
            )
            print(f"Navigated back to pricing page after capturing screenshot for plan {plan_number}")

        except Exception as e:
            # If something goes wrong, log it and take a screenshot
            print(f"Failed to click button for plan {plan_number}: {str(e)}")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/plan_yearly_failed_{plan_number}_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            self._store_test_results(f"Yearly Plan {plan_number} Registration", "Failed", screenshot_path)

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
