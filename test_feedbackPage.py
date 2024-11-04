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

class TestFeedbackPage:
    def setup_method(self, method):
        # Use headless Chrome for CI
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_feedbackPage(self):
        start_time = time.time()
        
        # Navigate to the main page
        self.driver.get("https://smoothmaths.co.uk/")
        self.driver.set_window_size(1296, 696)

        # Scroll to the bottom of the page to ensure the "Feedback" link is visible
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the "Feedback" link to be clickable and ensure it's visible
        try:
            feedback_link = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Feedback"))
            )
            # Scroll the feedback link into view to ensure visibility
            self.driver.execute_script("arguments[0].scrollIntoView(true);", feedback_link)
            time.sleep(1)  # Short pause to ensure the scrolling has completed
            feedback_link.click()
        except Exception as e:
            raise AssertionError(f"Could not locate or click the Feedback link. Error: {e}")

        # Add an explicit wait to ensure the form is fully loaded and interactable
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "wpforms-21990-field_2"))
        )

        # Fill in the feedback form
        self.driver.find_element(By.ID, "wpforms-21990-field_2").send_keys("Hanzila")
        self.driver.find_element(By.ID, "wpforms-21990-field_5").send_keys("testing")
        self.driver.find_element(By.ID, "wpforms-21990-field_4_5").click()  # Select feedback option
        self.driver.find_element(By.ID, "wpforms-submit-21990").click()

        # Wait for the confirmation message to appear
        try:
            confirmation_message = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".wpforms-confirmation-container-full p"))
            )

            if "Thanks for leaving a review!" in confirmation_message.text:
                # Save screenshot with timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_path = f"screenshots/feedback_confirmation_{timestamp}.png"
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                self.driver.save_screenshot(screenshot_path)

                # Store the test result as passed
                self._store_test_results("Test Feedback Page", "Passed", screenshot_path)
            else:
                # If the message is not correct, log failure with details
                self._log_failure("Unexpected confirmation message: " + confirmation_message.text)

        except Exception as e:
            # Log the failure in case the confirmation message is not found
            self._log_failure("Confirmation message did not appear. Error: " + str(e))

    def _log_failure(self, message):
        """Handles logging of failure details and stores them."""
        # Capture the page source for debugging
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        page_source = self.driver.page_source
        with open(f"screenshots/failed_page_source_{timestamp}.html", "w") as f:
            f.write(page_source)

        # Log the failure in CSV
        self._store_test_results("Test Feedback Page", "Failed", message)

    def _store_test_results(self, test_case, status, screenshot_path):
        # Save test results in a CSV file
        results = {
            "Test Case": [test_case],
            "Status": [status],
            "Screenshot": [screenshot_path]
        }
        df = pd.DataFrame(results)
        if not os.path.exists(CSV_FILE_PATH):
            df.to_csv(CSV_FILE_PATH, index=False)
        else:
            df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
