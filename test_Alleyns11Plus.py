import pytest
import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TestWordpressLogin:
    def setup_method(self, method):
        # Set up headless Chrome options for CI
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("window-size=1296,696")
        chrome_options.add_argument("--ignore-certificate-errors")

        self.driver: WebDriver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(60)
        self.driver.set_script_timeout(30)
        self.driver.implicitly_wait(10)

        # Ensure screenshots directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        self.vars = {}
        self.csv_file_path = "test_results.csv"
        logging.info("Setup completed.")

    def teardown_method(self, method):
        if self.driver:
            self.driver.quit()
            logging.info("Teardown completed. Driver quit.")

    def append_to_csv(self, results):
        df = pd.DataFrame(results)
        if os.path.exists(self.csv_file_path):
            df.to_csv(self.csv_file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(self.csv_file_path, mode='w', header=True, index=False)
        logging.info("Results appended to CSV.")

    def scroll_to_element(self, by, value):
        """Scroll directly to the element using JavaScript."""
        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((by, value))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logging.error(f"Element with locator ({by}, {value}) not found or not clickable.")
            raise

    def test_11Plus(self):
        # Start time to calculate test duration
        start_time = time.time()
        results = []

        # Hardcoded credentials (replace with your actual credentials)
        username = "hanzila@dovidigital.com"
        password = "Hanzila*183258"

        # Log in to WordPress
        try:
            self.driver.get("https://smoothmaths.co.uk/login/")
            logging.info("Navigated to login page.")

            # Dismiss any cookie consent or pop-up
            try:
                cookie_accept_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "cn-accept-cookie"))
                )
                cookie_accept_button.click()
                logging.info("Cookie consent dismissed.")
            except TimeoutException:
                logging.info("No cookie consent pop-up found.")

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "user_login"))
            )
            self.driver.find_element(By.ID, "user_login").send_keys(username)
            self.driver.find_element(By.ID, "user_pass").send_keys(password)
            self.driver.find_element(By.ID, "wp-submit").click()
            logging.info("Login form submitted.")

            # Verify login was successful by checking for a user-specific element
            try:
                # Wait for up to 20 seconds for login to complete
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.ID, "wp-admin-bar-my-account"))
                )
                logging.info("Login successful.")
            except TimeoutException:
                # Try to capture error message
                try:
                    error_message = self.driver.find_element(By.ID, "login_error").text
                    logging.error(f"Login failed with error message: {error_message}")
                except NoSuchElementException:
                    logging.error("Login failed. No error message found.")
                self.driver.save_screenshot("screenshots/login_failure.png")
                self.driver.quit()
                pytest.fail("Login failed.")
                return

        except Exception as e:
            logging.error(f"An unexpected error occurred during login: {e}")
            self.driver.save_screenshot("screenshots/login_failure.png")
            self.driver.quit()
            pytest.fail("Login failed due to an unexpected error.")
            return

        # Open the target page
        main_page_url = "https://smoothmaths.co.uk/11-plus-schools/alleyns-school/"
        self.driver.get(main_page_url)
        logging.info(f"Navigated to main page: {main_page_url}")

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

        # Locators for each answer paper using CSS selectors
        answer_paper_locators = [
            (By.CSS_SELECTOR, "a[href*='sample-examination-paper-1-answer-paper']"),  # First answer paper
            (By.CSS_SELECTOR, "a[href*='sample-examination-paper-2-answer-paper']"),  # Second answer paper
            (By.CSS_SELECTOR, "a[href*='sample-examination-answer-paper-1-2023']"),   # Third answer paper
            (By.CSS_SELECTOR, "a[href*='sample-examination-answer-paper-2-2023']")    # Fourth answer paper
        ]

        # Locators for each quiz using CSS selectors
        quiz_locators = [
            (By.CSS_SELECTOR, "a[href*='sample-examination-paper-1-online-quiz']"),  # First quiz
            (By.CSS_SELECTOR, "a[href*='sample-examination-paper-2-online-quiz']")   # Second quiz
        ]

        # Test each Answer Paper link
        for i, (by, value) in enumerate(answer_paper_locators):
            test_case_name = f"Answer Paper {i+1} Link Verification"
            try:
                # Scroll to the element and click
                answer_paper_link = self.scroll_to_element(by, value)
                answer_paper_link.click()
                logging.info(f"Clicked on {test_case_name} link.")

                # Verify the current URL
                expected_url = expected_answer_urls[i]
                WebDriverWait(self.driver, 15).until(
                    EC.url_to_be(expected_url)
                )

                # Wait for the page to load completely
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # Take a screenshot
                screenshot_path = f"screenshots/Alleyns_Answer_Paper_{i+1}.png"
                self.driver.save_screenshot(screenshot_path)
                logging.info(f"Screenshot saved to {screenshot_path}")

                # Log success status
                results.append({
                    "Test Case": test_case_name,
                    "Status": "Pass",
                    "Expected URL": expected_url,
                    "Actual URL": self.driver.current_url,
                    "Screenshot": screenshot_path
                })

            except Exception as e:
                logging.error(f"{test_case_name} failed: {str(e)}")
                screenshot_path = f"screenshots/Alleyns_error_Answer_Paper_{i+1}.png"
                self.driver.save_screenshot(screenshot_path)
                try:
                    actual_url = self.driver.current_url
                except:
                    actual_url = "N/A"
                results.append({
                    "Test Case": test_case_name,
                    "Status": f"Fail: {str(e)}",
                    "Expected URL": expected_answer_urls[i],
                    "Actual URL": actual_url,
                    "Screenshot": screenshot_path
                })

            finally:
                # Go back to the main page for the next link
                self.driver.get(main_page_url)
                logging.info("Returned to main page.")

        # Test each Quiz link
        for i, (by, value) in enumerate(quiz_locators):
            test_case_name = f"Quiz {i+1} Link Verification"
            try:
                # Scroll to each quiz link and click
                quiz_link = self.scroll_to_element(by, value)
                quiz_link.click()
                logging.info(f"Clicked on {test_case_name} link.")

                # Verify the current URL
                expected_url = expected_quiz_urls[i]
                WebDriverWait(self.driver, 15).until(
                    EC.url_to_be(expected_url)
                )

                # Wait for the page to load completely
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # Take a screenshot
                screenshot_path = f"screenshots/Quiz_{i+1}.png"
                self.driver.save_screenshot(screenshot_path)
                logging.info(f"Screenshot saved to {screenshot_path}")

                # Log success status
                results.append({
                    "Test Case": test_case_name,
                    "Status": "Pass",
                    "Expected URL": expected_url,
                    "Actual URL": self.driver.current_url,
                    "Screenshot": screenshot_path
                })

            except Exception as e:
                logging.error(f"{test_case_name} failed: {str(e)}")
                screenshot_path = f"screenshots/Alleyns_error_Quiz_{i+1}.png"
                self.driver.save_screenshot(screenshot_path)
                try:
                    actual_url = self.driver.current_url
                except:
                    actual_url = "N/A"
                results.append({
                    "Test Case": test_case_name,
                    "Status": f"Fail: {str(e)}",
                    "Expected URL": expected_quiz_urls[i],
                    "Actual URL": actual_url,
                    "Screenshot": screenshot_path
                })

            finally:
                # Go back to the main page for the next link
                self.driver.get(main_page_url)
                logging.info("Returned to main page.")

        # Log results to CSV
        self.append_to_csv(results)

        # Calculate duration
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Total test duration: {round(duration, 2)} seconds")
