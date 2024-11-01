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
        # Set up headless Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
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
        for _ in range(15):  # Increase retries to 15
            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((by, value))
                )
                return element
            except:
                self.driver.execute_script("window.scrollBy(0, 200);")
        raise Exception(f"Element with {by} and value {value} not found or not clickable")

    def scroll_back_to_main_page(self, main_page_url, locators):
        """Scroll down the main page until all elements in locators are loaded."""
        self.driver.get(main_page_url)
        time.sleep(2)
        for by, value in locators:
            try:
                self.scroll_to_element(by, value)
            except Exception as e:
                print(f"Error scrolling to element {by} with value {value}: {str(e)}")

    def test_11Plus(self):
        start_time = time.time()

        # Log in to WordPress
        self.driver.get("https://smoothmaths.co.uk/login/")
        self.driver.find_element(By.ID, "user_login").send_keys("hanzila@dovidigital.com")
        self.driver.find_element(By.ID, "user_pass").send_keys("Hanzila*183258")
        self.driver.find_element(By.ID, "wp-submit").click()
        
        # Open the target page
        main_page_url = "https://smoothmaths.co.uk/11-plus-schools/bancrofts-school/"
        self.driver.get(main_page_url)
        
        expected_answer_urls = [
            "https://smoothmaths.co.uk/bancrofts-school-11-plus-maths-sample-entrance-answer-paper-2024/",
            "https://smoothmaths.co.uk/bancrofts-school-11-plus-sample-maths-paper-2023-answer-paper/",
            "https://smoothmaths.co.uk/bancroft-schol-11-plus-sample-paper",
            "https://smoothmaths.co.uk/bancrofts-school-sample-11-plus-sample-maths-paper-2-answer-paper",
            "https://smoothmaths.co.uk/bancrofts-school-11-plus-entrance-examination-2022-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/bancrofts-school/bancrofts-school-11-plus-maths-sample-paper-2021-entry2-answer-paper",
            "https://smoothmaths.co.uk/bancroft-school-11plus-sample-2019-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/bancrofts-school/bancrofts-school-sample-11-plus-maths-paper-2018-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/bancrofts-school/bancrofts-school-sample-paper-11-maths-entrance-examination-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/bancrofts-school/bancroft-s-school-sample-11-plus-maths-paper-2-2016-answers-paper"
        ]
        
        expected_quiz_urls = [
            "https://smoothmaths.co.uk/bancrofts-school-sample-paper-11-maths-entrance-examination-online-quiz-2",
            "https://smoothmaths.co.uk/bancrofts-school-sample-11-plus-maths-paper-2018-online-quiz",
            "https://smoothmaths.co.uk/bancrofts-school-sample-paper-11-maths-entrance-examination-online-quiz",
            "https://smoothmaths.co.uk/bancrofts-school-sample-11-plus-maths-paper-2-2016-online-quiz"
        ]
        
        answer_paper_locators = [
            (By.CSS_SELECTOR, ".et_pb_blurb_1.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_3.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_5.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_7.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_9.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_11.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_14.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_16.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_19.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_22.et_pb_blurb .et_pb_module_header a")
        ]

        quiz_locators = [
            (By.XPATH, "//a[contains(@href, 'sample-paper-2021-entry-online-quiz')]"),
            (By.XPATH, "//a[contains(@href, 'entrance-examination-2018-online-quiz')]"),
            (By.XPATH, "//a[contains(@href, 'entrance-examination-2017-online-quiz')]"),
            (By.XPATH, "//a[contains(@href, 'entrance-examination-2016-online-quiz')]")
        ]

        results = []

        # Test each Answer Paper link
        for i, (by, value) in enumerate(answer_paper_locators):
            try:
                answer_paper_link = self.scroll_to_element(by, value)
                answer_paper_link.click()
                
                WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_answer_urls[i]))
                time.sleep(10)
                screenshot_path = f"screenshots/Bancroft_Answer_Paper_{i+1}.png"
                self.driver.save_screenshot(screenshot_path)
                
                results.append({
                    "Test Case": f"Answer Paper {i+1} Link Verification",
                    "Status": "Pass",
                    "Expected URL": expected_answer_urls[i],
                    "Actual URL": self.driver.current_url,
                    "Screenshot": screenshot_path
                })

            except Exception as e:
                screenshot_path = f"screenshots/Bancroft_error_Answer_Paper_{i+1}.png"
                self.driver.save_screenshot(screenshot_path)
                
                results.append({
                    "Test Case": f"Answer Paper {i+1} Link Verification",
                    "Status": f"Fail: {str(e)}",
                    "Expected URL": expected_answer_urls[i],
                    "Actual URL": self.driver.current_url if self.driver.current_url else "N/A",
                    "Screenshot": screenshot_path
                })

            self.scroll_back_to_main_page(main_page_url, answer_paper_locators + quiz_locators)

        # Test each Quiz link
        for i, (by, value) in enumerate(quiz_locators):
            try:
                quiz_link = self.scroll_to_element(by, value)
                self.driver.execute_script("arguments[0].click();", quiz_link)

                WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_quiz_urls[i]))

                time.sleep(10)
                screenshot_path = f"screenshots/Bancroft_Quiz_{i+1}.png"
                self.driver.save_screenshot(screenshot_path)
                
                results.append({
                    "Test Case": f"Quiz {i+1} Link Verification",
                    "Status": "Pass",
                    "Expected URL": expected_quiz_urls[i],
                    "Actual URL": self.driver.current_url,
                    "Screenshot": screenshot_path
                })

            except Exception as e:
                screenshot_path = f"screenshots/Bancroft_error_Quiz_{i+1}.png"
                self.driver.save_screenshot(screenshot_path)
                
                results.append({
                    "Test Case": f"Quiz {i+1} Link Verification",
                    "Status": f"Fail: {str(e)}",
                    "Expected URL": expected_quiz_urls[i],
                    "Actual URL": self.driver.current_url if self.driver.current_url else "N/A",
                    "Screenshot": screenshot_path
                })

            self.scroll_back_to_main_page(main_page_url, answer_paper_locators + quiz_locators)
        
        self.append_to_csv(results)

        end_time = time.time()
        duration = end_time - start_time
        print(f"Total test duration: {round(duration, 2)} seconds")
