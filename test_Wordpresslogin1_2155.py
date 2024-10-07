import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd
import datetime

# CSV file path to store all test results
CSV_FILE_PATH = "test_results.csv"

class TestWordpressLogin:
    def setup_method(self, method):
        # Set up headless Chrome options for CI
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1296, 696)

        # Ensure screenshots directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def teardown_method(self, method):
        # Close the browser after each test
        self.driver.quit()

    def append_to_csv(self, results):
        """Append the test results to the CSV file."""
        if not os.path.exists(CSV_FILE_PATH):
            df = pd.DataFrame(results)
            df.to_csv(CSV_FILE_PATH, index=False)  # Write a new file if it doesn't exist
        else:
            df = pd.DataFrame(results)
            df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)  # Append to existing file

    def test_login(self):
        start_time = time.time()

        # Navigate to the login page
        self.driver.get("https://smoothmaths.co.uk/login")

        # Step 2: Fill in the login form
        self.driver.find_element(By.ID, "user_login").send_keys("Testing")  
        self.driver.find_element(By.ID, "user_pass").send_keys("Testing*183258")  
        self.driver.find_element(By.ID, "wp-submit").click()

        try:
            # Step 3: Wait for either the homepage or an error message to load
            WebDriverWait(self.driver, 10).until(EC.url_contains("smoothmaths.co.uk"))

            # Step 4: Assert that we have been redirected to the homepage
            assert self.driver.current_url == "https://smoothmaths.co.uk/", "Login failed or not redirected to the homepage."
            screenshot_path = f"screenshots/successful_login_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            self.driver.save_screenshot(screenshot_path)  # Save a screenshot for successful login
            status = "Passed"

        except Exception as e:
            status = "Failed"
            screenshot_path = f"screenshots/login_failed_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            self.driver.save_screenshot(screenshot_path)

        # Record end time and calculate duration
        end_time = time.time()
        duration = end_time - start_time

        # Prepare results for CSV
        results = {
            "Test Case": ["Test Login"],
            "Status": [status],
            "Duration (seconds)": [round(duration, 2)],
            "Screenshot": [screenshot_path]
        }

        # Append results to the CSV file
        self.append_to_csv(results)
