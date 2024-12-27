import pytest
import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CSV file path to store all test results
CSV_FILE_PATH = "test_results.csv"

class TestBlackheathAnswers:
    def setup_method(self, method):
        # Set up headless Chrome options for CI (GitHub workflows)
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
        
        # Clear cache before starting the test
        chrome_options.add_argument("--disable-cache")

        # Create the driver with a longer timeout
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(180)  # Increased timeout for page loads
        self.driver.set_script_timeout(60)      # Increased timeout for script execution
        self.driver.implicitly_wait(30)         # Increased implicit wait

        # Ensure screenshots directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        
        self.vars = {}
  
    def teardown_method(self, method):
        # Quit the driver after each test
        self.driver.quit()

    def append_to_csv(self, results):
        """Append the test results to a CSV file."""
        df = pd.DataFrame(results)
        try:
            if os.path.exists(CSV_FILE_PATH):
                df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
            else:
                df.to_csv(CSV_FILE_PATH, mode='w', header=True, index=False)
            print("Successfully appended to CSV.")
        except Exception as e:
            print(f"Error appending to CSV: {e}")

    def scroll_and_click(self, locator, screenshot_name):
        """Scroll to an element, click it, and save a screenshot."""
        element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()
        
        # Save screenshot after clicking the element
        screenshot_path = f"screenshots/{screenshot_name}.png"
        self.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def test_blackheath_answers(self):
        # Start time to calculate test duration
        start_time = time.time()

        # Log in to SmoothMaths
        self.driver.get("https://smoothmaths.co.uk/login/")
        self.driver.find_element(By.ID, "user_login").send_keys("hanzila@dovidigital.com")
        self.driver.find_element(By.ID, "user_pass").send_keys("Hanzila*183258")
        self.driver.find_element(By.ID, "user_pass").send_keys(Keys.ENTER)
        
        # Step 2: Navigate to the main page
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Blackheath High School']")))
        self.driver.get("https://smoothmaths.co.uk/11-plus-schools/blackheath-high-school/")
        
        # Expected URLs for each answer paper
        expected_answer_urls = [
            "https://smoothmaths.co.uk/blackheath-high-school-11-plus-sample-examination-answer-paper-2024/",
            "https://smoothmaths.co.uk/11-plus-schools/blackheath-high-school/11-entrance-and-scholarship-examination-mathematics-practice-paper-answer-paper/"
        ]

        # Locators for each answer paper
        answer_paper_locators = [
            (By.CSS_SELECTOR, ".et_pb_blurb_1.et_pb_blurb .et_pb_module_header a", "First_Answer_Paper"),  
            (By.CSS_SELECTOR, ".et_pb_blurb_4.et_pb_blurb .et_pb_module_header a", "Second_Answer_Paper")
        ]

        results = []

        # Test each Answer Paper link
        for i, (by, value, screenshot_name) in enumerate(answer_paper_locators):
            try:
                # Scroll to the element and click it
                self.scroll_and_click((by, value), screenshot_name)

                # Verify the current URL
                WebDriverWait(self.driver, 30).until(EC.url_to_be(expected_answer_urls[i]))
                
                # Log current URL for debugging
                print(f"Navigated to: {self.driver.current_url}")

                # Log success status
                results.append({
                    "Test Case": f"Answer Paper {i+1} Link Verification",
                    "Status": "Pass",
                    "Expected URL": expected_answer_urls[i],
                    "Actual URL": self.driver.current_url,
                    "Screenshot": f"screenshots/{screenshot_name}.png"
                })

            except Exception as e:
                # Capture any errors and log failure status
                screenshot_path = f"screenshots/Error_{screenshot_name}.png"
                self.driver.save_screenshot(screenshot_path)
                
                results.append({
                    "Test Case": f"Answer Paper {i+1} Link Verification",
                    "Status": f"Fail: {str(e)}",
                    "Expected URL": expected_answer_urls[i],
                    "Actual URL": self.driver.current_url if self.driver.current_url else "N/A",
                    "Screenshot": screenshot_path
                })

            # Go back to the main page for the next link
            self.driver.get("https://smoothmaths.co.uk/11-plus-schools/blackheath-high-school/")
            time.sleep(2)

        # Append results to CSV
        self.append_to_csv(results)

        # Calculate the total test duration
        end_time = time.time()
        duration = end_time - start_time
        print(f"Total test duration: {round(duration, 2)} seconds")
