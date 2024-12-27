import pytest
import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

# CSV file path to store all test results
CSV_FILE_PATH = "test_results.csv"

class TestBlackheathanswers:
    def setup_method(self, method):
        # Set up Chrome options to disable cache
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("window-size=1382,744")
        chrome_options.add_argument("--disable-cache")  # Disable cache
        chrome_options.add_argument("--remote-debugging-port=9222")  # Fix for headless issues

        # Add this option to prevent cache in headless mode
        chrome_options.add_argument("--disk-cache-dir=/dev/null")  # Disable disk cache
        chrome_options.add_argument("--headless")  # Headless mode for CI/CD

        # Start Chrome with the specified options
        self.driver = webdriver.Chrome(options=chrome_options)
        self.vars = {}

        # Ensure screenshots directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def teardown_method(self, method):
        self.driver.quit()

    def append_to_csv(self, results):
        df = pd.DataFrame(results)
        try:
            if os.path.exists(CSV_FILE_PATH):
                df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
            else:
                df.to_csv(CSV_FILE_PATH, mode='w', header=True, index=False)
            print("Successfully appended to CSV.")
        except Exception as e:
            print(f"Error appending to CSV: {e}")

    def clear_cache(self):
        """ Clear cache between tests """
        self.driver.delete_all_cookies()  # This clears cookies, helping to clear cache between tests

    def test_blackheathanswers(self):
        # Clear cache before each test to ensure fresh load
        self.clear_cache()

        # Log in to SmoothMaths
        self.driver.get("https://smoothmaths.co.uk/login/")
        self.driver.find_element(By.ID, "user_login").send_keys("hanzila@dovidigital.com")
        self.driver.find_element(By.ID, "user_pass").send_keys("Hanzila*183258")
        self.driver.find_element(By.ID, "user_pass").send_keys(Keys.ENTER)

        # Wait for login to complete and navigate to the main page
        WebDriverWait(self.driver, 10).until(expected_conditions.url_changes("https://smoothmaths.co.uk/login/"))
        self.driver.get("https://smoothmaths.co.uk/11-plus-schools/blackheath-high-school/")

        # Click on the first answer paper link
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, "Answer Paper")))
        answer_paper_link = self.driver.find_element(By.LINK_TEXT, "Answer Paper")
        answer_paper_link.click()

        # Wait for the first answer paper to open and verify the link
        WebDriverWait(self.driver, 10).until(expected_conditions.url_to_be("https://smoothmaths.co.uk/blackheath-high-school-11-plus-sample-examination-answer-paper-2024/"))
        current_url = self.driver.current_url
        expected_url = "https://smoothmaths.co.uk/blackheath-high-school-11-plus-sample-examination-answer-paper-2024/"

        results = []
        if current_url != expected_url:
            screenshot_path = f"screenshots/Blackheath_error_Answer_Paper_1.png"
            self.driver.save_screenshot(screenshot_path)
            results.append({
                "Test Case": "First Answer Paper Link Verification",
                "Status": f"Fail: Expected URL {expected_url}, but got {current_url}",
                "Expected URL": expected_url,
                "Actual URL": current_url,
                "Screenshot": screenshot_path
            })
        else:
            screenshot_path = f"screenshots/Blackheath_Answer_Paper_1.png"
            self.driver.save_screenshot(screenshot_path)
            results.append({
                "Test Case": "First Answer Paper Link Verification",
                "Status": "Pass",
                "Expected URL": expected_url,
                "Actual URL": current_url,
                "Screenshot": screenshot_path
            })

        # Return to the main page
        self.driver.get("https://smoothmaths.co.uk/11-plus-schools/blackheath-high-school/")

        # Scroll to the second answer paper link and click it
        second_answer_paper_link = self.driver.find_element(By.LINK_TEXT, "11 Entrance and Scholarship Examination Mathematics Practice Paper Answer Paper")
        ActionChains(self.driver).move_to_element(second_answer_paper_link).perform()
        second_answer_paper_link.click()

        # Wait for the second answer paper to open and verify the link
        WebDriverWait(self.driver, 10).until(expected_conditions.url_to_be("https://smoothmaths.co.uk/11-plus-schools/blackheath-high-school/11-entrance-and-scholarship-examination-mathematics-practice-paper-answer-paper"))
        current_url = self.driver.current_url
        expected_url = "https://smoothmaths.co.uk/11-plus-schools/blackheath-high-school/11-entrance-and-scholarship-examination-mathematics-practice-paper-answer-paper"

        if current_url != expected_url:
            screenshot_path = f"screenshots/Blackheath_error_Answer_Paper_2.png"
            self.driver.save_screenshot(screenshot_path)
            results.append({
                "Test Case": "Second Answer Paper Link Verification",
                "Status": f"Fail: Expected URL {expected_url}, but got {current_url}",
                "Expected URL": expected_url,
                "Actual URL": current_url,
                "Screenshot": screenshot_path
            })
        else:
            screenshot_path = f"screenshots/Blackheath_Answer_Paper_2.png"
            self.driver.save_screenshot(screenshot_path)
            results.append({
                "Test Case": "Second Answer Paper Link Verification",
                "Status": "Pass",
                "Expected URL": expected_url,
                "Actual URL": current_url,
                "Screenshot": screenshot_path
            })

        # Append results to CSV
        self.append_to_csv(results)
