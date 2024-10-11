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

class TestYearlyPlans():
    def setup_method(self, method):
        # Use headless Chrome for CI
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1920, 1080)  # Larger window size to capture more content

        # Ensure screenshots directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def teardown_method(self, method):
        self.driver.quit()

    def test_yearly_pricing_plans(self):
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
            
            # List of expected URLs for the yearly registration pages (assumed based on plan names)
            plan_urls = [
                "https://smoothmaths.co.uk/register/11-plus-answers-solutions/",
                "https://smoothmaths.co.uk/register/11-plus-answers-quizzes/",
                "https://smoothmaths.co.uk/register/13-plus-answers-solutions/",
                "https://smoothmaths.co.uk/register/13-plus-answers-quizzes/",
                "https://smoothmaths.co.uk/register/igcse-gcse-mathematics-solutions/"
            ]

            # CSS Selectors for the Yearly Register buttons (assuming the buttons are in the order shown in the screenshot)
            button_selectors = [
                "a[href*='11-plus-answers-solutions']",
                "a[href*='11-plus-answers-quizzes']",
                "a[href*='13-plus-answers-solutions']",
                "a[href*='13-plus-answers-quizzes']",
                "a[href*='igcse-gcse-mathematics-solutions']"
            ]

            # Iterate through each yearly plan's register button
            for index, expected_url in enumerate(plan_urls):
                try:
                    print(f"Locating button for yearly plan {index+1}")
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
                    print(f"Clicking on 'Register' button for yearly plan {index+1}")
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

                    print(f"Yearly plan {index+1} registration status: {status}")

                    # Scroll down slightly to ensure the form is centered properly
                    self.driver.execute_script("window.scrollTo(0, 500);")
                    time.sleep(2)  # Small pause to ensure page is fully loaded

                    # Take a screenshot of the registration page after successful navigation
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    registration_screenshot_path = f"screenshots/yearly_plan_{index+1}_{status}_{timestamp}.png"
                    self.driver.save_screenshot(registration_screenshot_path)

                    # Record the test result
                    self._store_test_results(f"Yearly Plan {index+1} Registration", status, registration_screenshot_path)

                    # Go back to the pricing page for the next iteration
                    self.driver.get(pricing_page)
                    WebDriverWait(self.driver, 60).until(
                        EC.url_to_be(pricing_page)
                    )
                
                except Exception as e:
                    # Log the exception and continue to the next iteration
                    print(f"Exception occurred for yearly plan {index+1}: {str(e)}")
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    failed_screenshot_path = f"screenshots/failed_yearly_plan_{index+1}_{timestamp}.png"
                    self.driver.save_screenshot(failed_screenshot_path)
                    self._store_test_results(f"Yearly Plan {index+1} Registration", "Failed", failed_screenshot_path)

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
