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
  
    def scroll_to_element(self, by, value):
        """Scroll incrementally until the element is in view and clickable."""
        for _ in range(15):  # Increase the number of scroll attempts
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((by, value))
                )
                return element
            except:
                # Incrementally scroll down by 300px if the element is not yet clickable
                self.driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(1)  # Pause briefly after each scroll
        raise Exception("Element not found or not clickable")

    def test_11Plus(self):
        # Start time to calculate test duration
        start_time = time.time()

        self.driver.get("https://smoothmaths.co.uk/login/")
        self.driver.find_element(By.ID, "user_login").send_keys("hanzila@dovidigital.com")
        self.driver.find_element(By.ID, "user_pass").send_keys("Hanzila*183258")
        self.driver.find_element(By.ID, "wp-submit").click()
        
        main_page_url = "https://smoothmaths.co.uk/11-plus-schools/highgate-school/"
        self.driver.get(main_page_url)

        expected_answer_urls = [
            "https://smoothmaths.co.uk/11-plus-schools/highgate-school/entrance-examination-for-entry-into-year-7-11-example-question-mathematics-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/highgate-school/mathematics-sample-11-plus-paper-a-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/highgate-school/highgate-school-11-plus-assessment-sample-mathematics-test-b-answers-paper",
            "https://smoothmaths.co.uk/highgate-school-sample-test-c"
        ]

        answer_paper_locators = [
            (By.CSS_SELECTOR, ".et_pb_blurb_1.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_4.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_7.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_10.et_pb_blurb .et_pb_module_header a")
        ]


        results = []

        # Test each Answer Paper link
        for i, (by, value) in enumerate(answer_paper_locators):
            try:
                # Scroll to the element and get the clickable element
                answer_paper_link = self.scroll_to_element(by, value)
                answer_paper_link.click()
                
                # Verify the current URL
                WebDriverWait(self.driver, 15).until(EC.url_to_be(expected_answer_urls[i]))
                
                # Assert the URL is correct, if not, raise an AssertionError
                assert self.driver.current_url == expected_answer_urls[i], f"Expected URL to be {expected_answer_urls[i]}, but got {self.driver.current_url}"
                
                # Wait 5 seconds before taking a screenshot
                time.sleep(5)
                screenshot_path = f"screenshots/Highgate_Answer_Paper_{i+1}.png"
                self.driver.save_screenshot(screenshot_path)
                
                # Log success status
                results.append({
                    "Test Case": f"Answer Paper {i+1} Link Verification",
                    "Status": "Pass",
                    "Expected URL": expected_answer_urls[i],
                    "Actual URL": self.driver.current_url,
                    "Screenshot": screenshot_path
                })

            except Exception as e:
                # Capture any errors and log failure status
                screenshot_path = f"screenshots/HighGate_error_Answer_Paper_{i+1}.png"
                self.driver.save_screenshot(screenshot_path)
                
                results.append({
                    "Test Case": f"Answer Paper {i+1} Link Verification",
                    "Status": f"Fail: {str(e)}",
                    "Expected URL": expected_answer_urls[i],
                    "Actual URL": self.driver.current_url if self.driver.current_url else "N/A",
                    "Screenshot": screenshot_path
                })

            # Go back to the main page for the next link
            self.driver.get(main_page_url)
            time.sleep(3)


        # Log results to CSV
        self.append_to_csv(results)

        # Calculate duration
        end_time = time.time()
        duration = end_time - start_time
        print(f"Total test duration: {round(duration, 2)} seconds")
