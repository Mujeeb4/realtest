import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd

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
        
        # Expected URLs for each answer paper
        expected_urls = [
            "https://smoothmaths.co.uk/11-plus-schools/alleyns-school/allyens-11-maths-sample-examination-paper-1-answer-paper/",
            "https://smoothmaths.co.uk/11-plus-schools/alleyns-school/allyens-11-maths-sample-examination-paper-2-answer-paper/",
            "https://smoothmaths.co.uk/11-plus-schools/alleyns-school/allyens-11-maths-sample-examination-paper-1-2023-answer-paper/",
            "https://smoothmaths.co.uk/11-plus-schools/alleyns-school/allyens-11-maths-sample-examination-paper-2-2023-answer-paper/"
        ]
        
        # XPaths for each answer paper
        answer_paper_xpaths = [
            "(//div[contains(@class, 'et_pb_blurb') and .//a[contains(text(), 'Answer Paper')]])[1]//a",
            "(//div[contains(@class, 'et_pb_blurb') and .//a[contains(text(), 'Answer Paper')]])[2]//a",
            "(//div[contains(@class, 'et_pb_blurb') and .//a[contains(text(), 'Answer Paper')]])[3]//a",
            "(//div[contains(@class, 'et_pb_blurb') and .//a[contains(text(), 'Answer Paper')]])[4]//a"
        ]

        results = []

        for i, xpath in enumerate(answer_paper_xpaths):
            try:
                # Scroll down a bit to ensure visibility of the link
                self.driver.execute_script("window.scrollBy(0, 300);")
                
                # Click on the answer paper link
                answer_paper_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                answer_paper_link.click()
                
                # Verify the current URL
                WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_urls[i]))
                
                # Assert the URL is correct, if not, raise an AssertionError
                assert self.driver.current_url == expected_urls[i], f"Expected URL to be {expected_urls[i]}, but got {self.driver.current_url}"
                
                # Capture screenshot
                screenshot_path = f"screenshots/Answer_Paper_{i+1}.png"
                self.driver.save_screenshot(screenshot_path)
                
                # Log success status
                results.append({
                    "Test Case": f"Answer Paper {i+1} Link Verification",
                    "Status": "Pass",
                    "Expected URL": expected_urls[i],
                    "Actual URL": self.driver.current_url,
                    "Screenshot": screenshot_path
                })

            except Exception as e:
                # Capture any errors and log failure status
                screenshot_path = f"screenshots/error_Answer_Paper_{i+1}.png"
                self.driver.save_screenshot(screenshot_path)
                
                results.append({
                    "Test Case": f"Answer Paper {i+1} Link Verification",
                    "Status": f"Fail: {str(e)}",
                    "Expected URL": expected_urls[i],
                    "Actual URL": self.driver.current_url if self.driver.current_url else "N/A",
                    "Screenshot": screenshot_path
                })

            # Go back to the main page for the next link
            self.driver.back()
        
        # Log results to CSV
        self.append_to_csv(results)

        # Calculate duration
        end_time = time.time()
        duration = end_time - start_time
        print(f"Total test duration: {round(duration, 2)} seconds")
