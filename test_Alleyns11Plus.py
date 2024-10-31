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
        for _ in range(10):  # Try scrolling up to 10 times
            try:
                element = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable((by, value))
                )
                return element
            except:
                # Incrementally scroll down by 200px if the element is not yet clickable
                self.driver.execute_script("window.scrollBy(0, 200);")
        raise Exception("Element not found or not clickable")

    def capture_screenshot(self, name, is_error=False):
        """Capture screenshot with specific naming for success and failure."""
        directory = "screenshots"
        filename = f"{directory}/{('error_' if is_error else 'success_')}{name}.png"
        self.driver.save_screenshot(filename)
        return filename

    def test_11Plus(self):
        # Start time to calculate test duration
        start_time = time.time()

        # Log in to WordPress
        self.driver.get("https://smoothmaths.co.uk/login/")
        self.driver.find_element(By.ID, "user_login").send_keys("hanzila@dovidigital.com")
        self.driver.find_element(By.ID, "user_pass").send_keys("Hanzila*183258")
        self.driver.find_element(By.ID, "wp-submit").click()
        
        # Open the target page
        main_page_url = "https://smoothmaths.co.uk/11-plus-schools/alleyns-school/"
        self.driver.get(main_page_url)
        
        # Expected URLs for each answer paper
        expected_answer_urls = [
            "https://smoothmaths.co.uk/11-plus-schools/alleyns-school/allyens-11-maths-sample-examination-paper-1-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/alleyns-school/alleyns-11-maths-sample-examination-paper-2-answer-paper",
            "https://smoothmaths.co.uk/alleyns-school-11-plus-maths-sample-examination-answer-paper-1-2023",
            "https://smoothmaths.co.uk/alleyns-school-11-plus-maths-sample-examination-answer-paper-2-2023"
        ]
        
        # Expected URLs for each quiz
        expected_quiz_urls = [
            "https://smoothmaths.co.uk/allyens-11-maths-sample-examination-paper-1-online-quiz",
            "https://smoothmaths.co.uk/alleyns-11-maths-sample-examination-paper-2-online-quiz"
        ]
        
        # Locators for each answer paper, using XPath for the fourth answer paper
        answer_paper_locators = [
            (By.CSS_SELECTOR, ".et_pb_blurb_1 .et_pb_module_header a"),  # First answer paper
            (By.CSS_SELECTOR, ".et_pb_blurb_4 .et_pb_module_header a"),  # Second answer paper
            (By.CSS_SELECTOR, ".et_pb_blurb_7 .et_pb_module_header a"),  # Third answer paper
            (By.XPATH, "//a[contains(@href, 'sample-examination-answer-paper-2-2023')]")  # Fourth answer paper using XPath
        ]

        # XPath selectors for each quiz based on screenshots
        quiz_locators = [
            (By.XPATH, "//a[contains(@href, 'sample-examination-paper-1-online-quiz')]"),  # First quiz
            (By.XPATH, "//a[contains(@href, 'sample-examination-paper-2-online-quiz')]")   # Second quiz
        ]

        results = []

        # Test each Answer Paper link
        for i, (by, value) in enumerate(answer_paper_locators):
            try:
                # Scroll to the element and get the clickable element
                answer_paper_link = self.scroll_to_element(by, value)
                answer_paper_link.click()
                
                # Scroll down slightly after clicking
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(1)  # Brief pause to allow the page to settle after scrolling
                
                # Verify the current URL
                WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_answer_urls[i]))
                
                # Capture success screenshot
                screenshot_path = self.capture_screenshot(f"Answer_Paper_{i+1}", is_error=False)
                
                # Log success status
                results.append({
                    "Test Case": f"Answer Paper {i+1} Link Verification",
                    "Status": "Pass",
                    "Expected URL": expected_answer_urls[i],
                    "Actual URL": self.driver.current_url,
                    "Screenshot": screenshot_path
                })

            except Exception as e:
                # Capture error screenshot
                screenshot_path = self.capture_screenshot(f"Answer_Paper_{i+1}", is_error=True)
                
                results.append({
                    "Test Case": f"Answer Paper {i+1} Link Verification",
                    "Status": f"Fail: {str(e)}",
                    "Expected URL": expected_answer_urls[i],
                    "Actual URL": self.driver.current_url if self.driver.current_url else "N/A",
                    "Screenshot": screenshot_path
                })

            # Go back to the main page for the next link
            self.driver.get(main_page_url)
            time.sleep(2)

        # Test each Quiz link
        for i, (by, value) in enumerate(quiz_locators):
            try:
                # Scroll to each quiz link incrementally
                quiz_link = self.scroll_to_element(by, value)
                
                # Use JavaScript to click the quiz link
                self.driver.execute_script("arguments[0].click();", quiz_link)
                
                # Scroll down slightly after clicking the quiz link
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(1)  # Brief pause to allow the page to settle after scrolling
                
                # Verify the current URL
                WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_quiz_urls[i]))
                
                # Capture success screenshot
                screenshot_path = self.capture_screenshot(f"Quiz_{i+1}", is_error=False)
                
                # Log success status
                results.append({
                    "Test Case": f"Quiz {i+1} Link Verification",
                    "Status": "Pass",
                    "Expected URL": expected_quiz_urls[i],
                    "Actual URL": self.driver.current_url,
                    "Screenshot": screenshot_path
                })

            except Exception as e:
                # Capture error screenshot
                screenshot_path = self.capture_screenshot(f"Quiz_{i+1}", is_error=True)
                
                results.append({
                    "Test Case": f"Quiz {i+1} Link Verification",
                    "Status": f"Fail: {str(e)}",
                    "Expected URL": expected_quiz_urls[i],
                    "Actual URL": self.driver.current_url if self.driver.current_url else "N/A",
                    "Screenshot": screenshot_path
                })

            # Go back to the main page for the next link
            self.driver.get(main_page_url)
            time.sleep(2)
        
        # Log results to CSV
        self.append_to_csv(results)

        # Calculate duration
        end_time = time.time()
        duration = end_time - start_time
        print(f"Total test duration: {round(duration, 2)} seconds")
