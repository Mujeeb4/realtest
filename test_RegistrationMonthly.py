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
            # Navigate directly to the pricing page
            self.driver.get(pricing_page)
            print("Navigating to the pricing page")

            # Wait for the page to load and verify we're on the pricing page
            WebDriverWait(self.driver, 60).until(
                EC.url_to_be(pricing_page)
            )
            print("Successfully navigated to pricing page")
            
            # Take a screenshot of the pricing page
            self.driver.save_screenshot("screenshots/pricing_page.png")

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
                try:
                    print(f"Locating button for plan {index+1}")
                    # Use XPath for the first button, then CSS Selectors for the rest
                    if index == 0:
                        locator = (By.XPATH, button_selectors[index])
                    else:
                        locator = (By.CSS_SELECTOR, button_selectors[index])

                    # Wait for the "Register" button to be present and clickable
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

                    # Click on the "Register" button using JavaScript in case of issues
                    print(f"Clicking on 'Register' button for plan {index+1}")
                    self.driver.execute_script("arguments[0].click();", register_button)

                    # Wait for the redirection to the registration page
                    print(f"Waiting for redirection to {expected_url}")
                    WebDriverWait(self.driver, 120).until(
                        EC.url_contains(expected_url)
                    )

                    # Check if we were redirected to the correct page
                    current_url = self.driver.current_url
                    print(f"Current URL after click: {current_url}")
                    if current_url == expected_url:
                        status = "Passed"
                    else:
                        status = "Failed"

                    print(f"Plan {index+1} registration status: {status}")

                    # Take a screenshot of the registration page after successful navigation
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    registration_screenshot_path = f"screenshots/registration_plan_{index+1}_{status}_{timestamp}.png"
                    self.driver.save_screenshot(registration_screenshot_path)

                    # Record the test result
                    self._store_test_results(f"Plan {index+1} Registration", status, registration_screenshot_path)

                    # Go back to the pricing page for the next iteration
                    self.driver.get(pricing_page)
                    WebDriverWait(self.driver, 60).until(
                        EC.url_to_be(pricing_page)
                    )
                
                except Exception as e:
                    # Log the exception and continue to the next iteration
                    print(f"Exception occurred for plan {index+1}: {str(e)}")
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    failed_screenshot_path = f"screenshots/failed_plan_{index+1}_{timestamp}.png"
                    self.driver.save_screenshot(failed_screenshot_path)
                    self._store_test_results(f"Plan {index+1} Registration", "Failed", failed_screenshot_path)

        except Exception as e:
            # Save a screenshot and record the test as failed if any exception occurs
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            failed_pricing_screenshot_path = f"screenshots/failed_pricing_plan_{timestamp}.png"
            self.driver.save_screenshot(failed_pricing_screenshot_path)
            self._store_test_results("Pricing Plan Test", "Failed", failed_pricing_screenshot_path)
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

