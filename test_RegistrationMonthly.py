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
            print("Navigating to the homepage")

            # Wait for the page to load and ensure "Join Now" button is clickable
            join_now_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.divi-life-cta-menu"))
            )
            print("Join Now button located")

            # Scroll into view if necessary
            self.driver.execute_script("arguments[0].scrollIntoView(true);", join_now_button)
            time.sleep(1)  # Allow time for scroll and rendering

            # Click the button
            join_now_button.click()
            print("Join Now button clicked")

            # Wait for navigation to the pricing page
            WebDriverWait(self.driver, 60).until(
                EC.url_to_be(pricing_page)
            )
            print("Navigated to pricing page")
            
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

            # Updated locators with XPath and CSS Selectors
            button_selectors = [
                "//a[contains(text(),'Register')]",  # XPath for the first button
                "a[href*='11-plus-answers-quizzes']",  # CSS Selector for the second button
                "a[href*='13-plus-answers-solutions']",  # CSS Selector for the third button
                "a[href*='13-plus-answers-quizzes']",  # CSS Selector for the fourth button
                "a[href*='igcse-gcse-mathematics-solutions']"  # CSS Selector for the fifth button
            ]

            # Iterate through each plan's register button
            for index, expected_url in enumerate(plan_urls):
                # Use XPath for the first button, then CSS Selectors for the rest
                if index == 0:
                    locator = (By.XPATH, button_selectors[index])
                else:
                    locator = (By.CSS_SELECTOR, button_selectors[index])

                print(f"Locating button for plan {index+1}")
                # Wait for the "Register" button to be present
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located(locator)
                )
                register_button = self.driver.find_element(*locator)

                # Ensure the button is visible and clickable
                WebDriverWait(self.driver, 60).until(
                    EC.visibility_of(register_button)
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
                time.sleep(1)  # Small pause to ensure the page scrolls

                # Click on the "Register" button for the current plan
                register_button.click()

                # Wait for the redirection to the registration page
                WebDriverWait(self.driver, 60).until(
                    EC.url_contains(expected_url)
                )

                # Check if we were redirected to the correct page
                if self.driver.current_url == expected_url:
                    status = "Passed"
                else:
                    status = "Failed"

                print(f"Plan {index+1} registration status: {status}")

                # Take a screenshot
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_path = f"screenshots/plan_{index+1}_{status}_{timestamp}.png"
                self.driver.save_screenshot(screenshot_path)

                # Record the test result
                self._store_test_results(f"Plan {index+1} Registration", status, screenshot_path)

                # Go back to the pricing page for the next iteration
                self.driver.get(pricing_page)
                WebDriverWait(self.driver, 60).until(
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
