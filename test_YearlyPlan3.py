import pytest
import time
import os
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, WebDriverException

# CSV file path to store test results
CSV_FILE_PATH = "test_results.csv"

class TestPlan3():
    def setup_method(self, method):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1920, 1080)

        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def teardown_method(self, method):
        self.driver.quit()

    def click_with_retry(self, locator, retries=3):
        attempts = 0
        while attempts < retries:
            try:
                element = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located(locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                self.driver.execute_script("arguments[0].click();", element)
                print(f"Element clicked successfully on attempt {attempts + 1}")
                return True
            except (TimeoutException, ElementClickInterceptedException, WebDriverException) as e:
                print(f"Failed to click element on attempt {attempts + 1}: {e}")
                attempts += 1
                time.sleep(2)
        print(f"Failed to click element after {retries} retries.")
        return False

    def navigate_with_retry(self, url, retries=3):
        attempts = 0
        while attempts < retries:
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 60).until(EC.url_to_be(url))
                return True
            except WebDriverException as e:
                print(f"Failed to navigate to {url} on attempt {attempts + 1}: {e}")
                attempts += 1
                time.sleep(5)
        return False

    def test_plan_3(self):
        start_time = time.time()
        pricing_page = "https://smoothmaths.co.uk/pricing/"
        expected_url = "https://smoothmaths.co.uk/register/13-plus-subscription-plan-yearly"

        try:
            if not self.navigate_with_retry(pricing_page):
                raise Exception("Failed to navigate to the pricing page after retries.")

            yearly_locator = (By.XPATH, "//span[@class='title' and contains(text(),'Yearly')]")
            if not self.click_with_retry(yearly_locator):
                raise Exception("Failed to click the Yearly button after retries.")

            time.sleep(2)
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//span[@class='title' and contains(text(),'Yearly')]"))
            )

            register_locator = (By.XPATH, "(//a[contains(text(),'Register') and contains(@href, 'yearly')])[3]")
            if not self.click_with_retry(register_locator):
                raise Exception("Failed to click the Register button for Plan 3 after retries.")

            WebDriverWait(self.driver, 120).until(EC.url_contains(expected_url))
            current_url = self.driver.current_url
            status = "Passed" if current_url == expected_url else "Failed"

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/plan_3_{status}_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            self._store_test_results("Plan 3 Registration", status, screenshot_path)

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/plan_3_failed_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            self._store_test_results("Plan 3 Registration", "Failed", screenshot_path)

        finally:
            end_time = time.time()
            duration = end_time - start_time
            print(f"Test duration for Plan 3: {round(duration, 2)} seconds")

    def _store_test_results(self, test_case, status, screenshot_path):
        results = {
            "Test Case": [test_case],
            "Status": [status],
            "Screenshot": [screenshot_path]
        }

        if not os.path.exists(CSV_FILE_PATH):
            pd.DataFrame(results).to_csv(CSV_FILE_PATH, index=False)
        else:
            pd.DataFrame(results).to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
