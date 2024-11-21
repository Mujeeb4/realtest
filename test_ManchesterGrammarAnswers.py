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

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for the page to load
            
            # Calculate new scroll height and compare with the last height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def scroll_and_click_all_papers(self, paper_locators, expected_urls, main_page_url):
        results = []

        for i, (by, value) in enumerate(paper_locators):
            try:
                # Scroll to the bottom to ensure all elements are loaded
                self.scroll_to_bottom()

                # Find and click the paper link
                answer_paper_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, value))
                )
                answer_paper_link.click()

                # Verify the URL matches the expected URL
                WebDriverWait(self.driver, 15).until(EC.url_to_be(expected_urls[i]))
                assert self.driver.current_url == expected_urls[i], \
                    f"Expected URL {expected_urls[i]}, but got {self.driver.current_url}"

                # Take a screenshot for verification
                screenshot_path = f"screenshots/Paper_{i + 1}.png"
                self.driver.save_screenshot(screenshot_path)

                # Log the success
                results.append({
                    "Test Case": f"Paper {i + 1} Verification",
                    "Status": "Pass",
                    "Expected URL": expected_urls[i],
                    "Actual URL": self.driver.current_url,
                    "Screenshot": screenshot_path
                })

            except Exception as e:
                # Log the failure
                screenshot_path = f"screenshots/Error_Paper_{i + 1}.png"
                self.driver.save_screenshot(screenshot_path)
                results.append({
                    "Test Case": f"Paper {i + 1} Verification",
                    "Status": f"Fail: {str(e)}",
                    "Expected URL": expected_urls[i],
                    "Actual URL": self.driver.current_url if self.driver.current_url else "N/A",
                    "Screenshot": screenshot_path
                })

            # Return to the main page for the next paper
            self.driver.get(main_page_url)
            time.sleep(2)

        return results

    def test_11Plus(self):
        # Start time to calculate test duration
        start_time = time.time()

        self.driver.get("https://smoothmaths.co.uk/login/")
        self.driver.find_element(By.ID, "user_login").send_keys("hanzila@dovidigital.com")
        self.driver.find_element(By.ID, "user_pass").send_keys("Hanzila*183258")
        self.driver.find_element(By.ID, "wp-submit").click()
        
        main_page_url = "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/"
        self.driver.get(main_page_url)

        expected_answer_urls = [
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2019-arithmetic-section-a-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2019-arithmetic-section-b-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2018-arithmetic-section-a-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2018-arithmetic-section-b-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2017-arithmetic-section-a",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2017-arithmetic-section-b-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2016-arithmetic-section-a-answer-paper",
            "https://smoothmaths.co.uk/the-manchester-grammar-school-11-plus-entrance-examination-2016-arithmetic-section-b",
            "https://smoothmaths.co.uk/the-manchester-grammar-school-11-plus-entrance-examination-2014-arithmetic-answer-paper-a",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2014-arithmetic-section-b-answer-paper",
            "https://smoothmaths.co.uk/the-manchester-grammar-school-11-plus-entrance-examination-2013-arithmetic-answer-paper-1",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2013-arithmetic-paper-2-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2012-arithmetic-paper-1-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2012-arithmetic-paper-2-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2011-arithmetic-paper-1-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2011-arithmetic-paper-2-answer-paper",
            "https://smoothmaths.co.uk/11-plus-schools/the-manchester-grammer-school/the-manchester-grammar-school-entrance-examination-2010-part-1-arithmetic-examination-answers-paper",
            "https://smoothmaths.co.uk/the-manchester-grammar-school-11-plus-entrance-examination-2010-arithmetic-answer-paper-2",
            "https://smoothmaths.co.uk/the-manchester-grammar-school-11-plus-2009-entrance-examination-arithmetic-answer-paper",
            "https://smoothmaths.co.uk/the-manchester-grammar-school-11-plus-entrance-examination-2009-section-2-answer-paper",
            "https://smoothmaths.co.uk/the-manchester-grammar-school-11-plus-entrance-examination-2008-section-1-answer-paper",
            "https://smoothmaths.co.uk/the-manchester-grammar-school-11-plus-entrance-examination-2008-part-2-answer-paper/"
        ]

        answer_paper_locators = [
            (By.CSS_SELECTOR, ".et_pb_blurb_1.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_4.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_7.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_10.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_13.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_16.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_19.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_22.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_24.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_26.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_29.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_31.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_34.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_37.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_40.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_43.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_46.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_49.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_51.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_53.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_55.et_pb_blurb .et_pb_module_header a"),
            (By.CSS_SELECTOR, ".et_pb_blurb_57.et_pb_blurb .et_pb_module_header a")

        ]


        results = self.scroll_and_click_all_papers(answer_paper_locators, expected_answer_urls, main_page_url)
        
        # Log results to CSV
        self.append_to_csv(results)

        # Calculate duration
        end_time = time.time()
        duration = end_time - start_time
        print(f"Total test duration: {round(duration, 2)} seconds")
