import pytest
import time
import os
import datetime
import pandas as pd  # <--- Add this import for pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestPlan2():
    def setup_method(self, method):
        # Use headless Chrome for CI
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1920, 1080) 

        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def teardown_method(self, method):
        self.driver.quit()

    def test_plan_2(self):
        start_time = time.time()
        pricing_page = "https://smoothmaths.co.uk/pricing/"
        expected_url = "https://smoothmaths.co.uk/register/11-plus-answers-quizzes/"

        try:
            self.driver.get(pricing_page)
            WebDriverWait(self.driver, 60).until(
                EC.url_to_be(pricing_page)
            )

            register_button = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='11-plus-answers-quizzes']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", register_button)

            WebDriverWait(self.driver, 120).until(
                EC.url_contains(expected_url)
            )
            current_url = self.driver.current_url
            status = "Passed" if current_url == expected_url else "Failed"

            time.sleep(2)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/plan_2_{status}_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            self._store_test_results("Plan 2 Registration", status, screenshot_path)

        except Exception as e:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/plan_2_failed_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            self._store_test_results("Plan 2 Registration", "Failed", screenshot_path)

        finally:
            end_time = time.time()
            print(f"Test duration for Plan 2: {round(end_time - start_time, 2)} seconds")

    def _store_test_results(self, test_case, status, screenshot_path):
        results = {"Test Case": [test_case], "Status": [status], "Screenshot": [screenshot_path]}
        if not os.path.exists("test_results.csv"):
            pd.DataFrame(results).to_csv("test_results.csv", index=False)
        else:
            pd.DataFrame(results).to_csv("test_results.csv", mode='a', header=False, index=False)
