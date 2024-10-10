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

class TestPricingPlans():
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

    def test_pricing_plans(self):
        start_time = time.time()
        pricing_page = "https://smoothmaths.co.uk/pricing/"
        
        try:
            # Navigate to the main page
            self.driver.get("https://smoothmaths.co.uk/")
            
            # Click on the "Join Now" button in the header
            join_now_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "JOIN NOW"))
            )
            join_now_button.click()

            # Navigate to pricing page and check if the URL is correct
            WebDriverWait(self.driver, 30).until(
                EC.url_to_be(pricing_page)
            )
            
            # Verify if we are on the pricing page
            assert self.driver.current_url == pricing_page, "Failed to navigate to pricing page"

            # List of expected URLs for the registration pages
            plan_urls = [
                "https://smoothmaths.co.uk/register/11-plus-subscription-plan/",
                "https://smoothmaths.co.uk/register/11-plus-answers-quizzes/",
                "https://smoothmaths.co.uk/register/13-plus-answers-solutions/",
                "https://smoothmaths.co.uk/register/13-plus-answers-quizzes/",
                "https://smoothmaths.co.uk/register/igcse-gcse-mathematics-solutions/"
            ]

            # Correct CSS selectors based on the provided screenshots
            button_selectors = [
                "a.et_pb_button.df_6707e2655e7f3_et_pb_button_0",
                "a.et_pb_button.df_6707e2655e7f3_et_pb_button_1",
                "a.et_pb_button.df_6707e2655e7f3_et_pb_button_2",
                "a.et_pb_button.df_6707e2655e7f3_et_pb_button_3",
                "a.et_pb_button.df_6707e2655e7f3_et_pb_button_4"
            ]

            # Iterate through each plan's register button
            for index, expected_url in enumerate(plan_urls):
                # Scroll to the "Register" button
                self.driver.execute_script("arguments[0].scrollIntoView();", 
                    self.driver.find_element(By.CSS_SELECTOR, button_selectors[index])
                )
                time.sleep(1)

                # Click on the "Register" button for the current plan
                register_button = self.driver.find_element(By.CSS_SELECTOR, button_selectors[index])
                register_button.click()

                # Wait for the redirection to the registration page
                WebDriverWait(self.driver, 30).until(
                    EC.url_contains(expected_url)
                )

                # Check if we were redirected to the correct page
                if self.driver.current_url == expected_url:
                    status = "Passed"
                else:
                    status = "Failed"

                # Take a screenshot
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_path = f"screenshots/plan_{index+1}_{status}_{timestamp}.png"
                self.driver.save_screenshot(screenshot_path)

                # Record the test result
                self._store_test_results(f"Plan {index+1} Registration", status, screenshot_path)

                # Go back to the pricing page for the next iteration
                self.driver.get(pricing_page)
                WebDriverWait(self.driver, 30).until(
                    EC.url_to_be(pricing_page)
                )

        except Exception as e:
            # Save a screenshot and record the test as failed if any exception occurs
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/failed_pricing_plan_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            self._store_test_results("Pricing Plan Test", "Failed", screenshot_path)
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
