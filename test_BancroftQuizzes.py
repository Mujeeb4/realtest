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
        # Set up Chrome options for debugging (headless mode removed)
        chrome_options = Options()
        # Remove headless mode for debugging
        # chrome_options.add_argument("--headless")  # Comment this line out
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
        
        self.results = []
  
    def teardown_method(self, method):
        # Save results to CSV after all tests
        self.append_to_csv(self.results)
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

        # Log in to WordPress
        self.driver.get("https://smoothmaths.co.uk/login/")
        self.driver.find_element(By.ID, "user_login").send_keys("hanzila@dovidigital.com")
        self.driver.find_element(By.ID, "user_pass").send_keys("Hanzila*183258")
        self.driver.find_element(By.ID, "wp-submit").click()
        
        # Open the target page
        main_page_url = "https://smoothmaths.co.uk/11-plus-schools/bancrofts-school/"
        self.driver.get(main_page_url)

        # Define CSS selectors for each quiz link
        quiz_selectors = [
            ".et_pb_blurb_12 a",  # Quiz 1
            ".et_pb_blurb_17 a",  # Quiz 2
            ".et_pb_blurb_20 a",  # Quiz 3
            ".et_pb_blurb_23 a"   # Quiz 4
        ]

        # Loop through each quiz using the CSS selectors
        for i, selector in enumerate(quiz_selectors, start=1):
            try:
                # Scroll to and locate each quiz element by its unique CSS selector
                quiz_element = self.scroll_to_element(By.CSS_SELECTOR, selector)
                quiz_element.click()

                # Wait for the new quiz window to open and switch to it
                WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
                self.driver.switch_to.window(self.driver.window_handles[1])

                # Wait briefly to ensure the page loads completely before taking a screenshot
                time.sleep(5)
                screenshot_path = f"screenshots/quiz_{i}.png"
                if self.driver.save_screenshot(screenshot_path):
                    print(f"Screenshot saved for Quiz {i}: {screenshot_path}")  # Confirmation print

                # Store test results for this quiz
                result = {
                    "Quiz": f"Quiz {i}",
                    "Link": self.driver.current_url,
                    "Screenshot": screenshot_path,
                    "Status": "Success"
                }
                self.results.append(result)

                # Close the quiz window and switch back to the main window
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])

            except Exception as e:
                # Capture a screenshot in case of failure
                screenshot_path = f"screenshots/quiz_{i}_error.png"
                if self.driver.save_screenshot(screenshot_path):
                    print(f"Error screenshot saved for Quiz {i}: {screenshot_path}")  # Confirmation print

                # If any error occurs, log it
                result = {
                    "Quiz": f"Quiz {i}",
                    "Link": None,
                    "Screenshot": screenshot_path,
                    "Status": f"Failed - {str(e)}"
                }
                self.results.append(result)
                continue

        # Calculate and log test duration
        end_time = time.time()
        test_duration = end_time - start_time
        self.results.append({"Test": "Total Duration", "Duration": f"{test_duration:.2f} seconds"})
