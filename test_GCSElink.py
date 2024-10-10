import pytest
import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test13Plus():
    def setup_method(self, method):
        # Set up Chrome options for headless execution (suitable for CI)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1296, 696)

        # Create directories for saving screenshots and CSV results
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        if not os.path.exists("results"):
            os.makedirs("results")

    def teardown_method(self, method):
        self.driver.quit()

    def test_13Plus(self):
        # Start the test timer
        start_time = time.time()

        try:
            # Navigate to the homepage
            self.driver.get("https://smoothmaths.co.uk/")

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "GCSE"))
            ).click()

            # Wait for the new page to load and check the URL
            expected_url = "https://smoothmaths.co.uk/gcse/"
            WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))
            current_url = self.driver.current_url

            # Take a screenshot of the 13 Plus page
            self.save_screenshot("GCSE_Page")

            # Check if the URL is correct
            if current_url == expected_url:
                status = "Passed"
                print("GCSE URL is correct")
            else:
                status = "Failed"
                print(f"Error: Expected URL '{expected_url}', but got '{current_url}'")

            # Record the test result in CSV
            end_time = time.time()
            self.save_test_results("GCSE Link Test", status, round(end_time - start_time, 2))

        except Exception as e:
            self.save_screenshot("GCSE_test_failed")
            self.save_test_results("GCSE Link Test", "Failed", str(e))
            raise AssertionError(f"Test failed: {e}")

    def save_screenshot(self, name):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = f"screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(screenshot_path)

    def save_test_results(self, test_case, status, duration_or_error):
        results_file = "results/test_results.csv"
        fieldnames = ["Test Case", "Status", "Duration/Error", "Timestamp"]

        # Create the CSV file and add headers if it doesn't exist
        if not os.path.exists(results_file):
            with open(results_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

        # Append the test result
        with open(results_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({
                "Test Case": test_case,
                "Status": status,
                "Duration/Error": duration_or_error,
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
