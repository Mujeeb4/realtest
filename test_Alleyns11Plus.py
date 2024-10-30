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
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("window-size=1296,696")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(60)
        self.driver.set_script_timeout(30)
        self.driver.implicitly_wait(10)

        # Ensure screenshots directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        
        self.vars = {}
  
    def teardown_method(self, method):
        self.driver.quit()

    def append_to_csv(self, results):
        df = pd.DataFrame(results)
        if os.path.exists(CSV_FILE_PATH):
            df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
        else:
            df.to_csv(CSV_FILE_PATH, mode='w', header=True, index=False)
  
    def test_11Plus(self):
        # Start time to calculate test duration
        start_time = time.time()

        # Log in to WordPress
        self.driver.get("https://smoothmaths.co.uk/login/")
        self.driver.find_element(By.ID, "user_login").send_keys("hanzila@dovidigital.com")
        self.driver.find_element(By.ID, "user_pass").send_keys("Hanzila*183258")
        self.driver.find_element(By.ID, "wp-submit").click()
        
        # Open the target page
        self.driver.get("https://smoothmaths.co.uk/11-plus-schools/alleyns-school/")
        
        try:
            # Click on the "Answer Paper" link
            self.driver.find_element(By.LINK_TEXT, "Answer Paper").click()
            
            # Scroll to the specific location on the page
            self.driver.execute_script("window.scrollTo(0, 30.66666603088379)")
            
            # Wait for the first answer paper link to appear and click it
            first_answer_paper = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".et_pb_blurb_4 .et_pb_blurb_container a"))
            )
            first_answer_paper.click()
            
            # Additional scroll if necessary
            self.driver.execute_script("window.scrollTo(0, 34)")
            
            # Check if the expected structure appears by locating an element within it
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".et_pb_blurb_7"))
            )
            
             # Capture screenshot before form submission
            self.capture_screenshot("First_Paper")
            
            # Go back to the previous page
            self.driver.back()
            
            # Scroll down and click the second answer paper link
            self.driver.execute_script("window.scrollTo(0, 1478.6666259765625)")
            second_answer_paper = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".et_pb_blurb_9 .et_pb_blurb_container a"))
            )
            second_answer_paper.click()

            # Additional scroll if necessary
            self.driver.execute_script("window.scrollTo(0, 34)")
            
            # Check if the expected structure appears by locating an element within it
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".et_pb_blurb_7"))
            )
            
             # Capture screenshot before form submission
            self.capture_screenshot("Second_Paper")
            
            # Set test status to pass
            status = "Pass"
        
        except Exception as e:
            # Capture any errors
            status = f"Fail: {str(e)}"
            screenshot_path = "screenshots/error_screenshot.png"
            self.driver.save_screenshot(screenshot_path)
        
        # Calculate duration and log results
        end_time = time.time()
        duration = end_time - start_time

        # Prepare results for CSV
        results = {
            "Test Case": ["Test Login and 11+ Paper Navigation"],
            "Status": [status],
            "Duration (seconds)": [round(duration, 2)],
            "Screenshot": [screenshot_path]
        }

        # Append results to the CSV file
        self.append_to_csv(results)
