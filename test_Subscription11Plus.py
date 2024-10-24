import pytest
import time
import os
import datetime
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# CSV file path to store test results
CSV_FILE_PATH = "test_results.csv"

class TestSubscription:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

        # Ensure screenshots directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        yield
        # Save screenshot before quitting the driver
        self.capture_screenshot("final_screenshot")
        self.driver.quit()

    def capture_screenshot(self, name):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.abspath(f"screenshots/{name}_{timestamp}.png")
        if self.driver.save_screenshot(screenshot_path):
            print(f"Screenshot saved successfully: {screenshot_path}")
        else:
            print(f"Failed to save screenshot: {screenshot_path}")
        return screenshot_path

    def test_subscription(self):
        start_time = time.time()
        status = "Failed"
        screenshot_path = ""
        try:
            # Generate a random email address
            random_number = random.randint(1000, 9999)
            random_email = f"testing{random_number}@gmail.com"

            # Navigate to subscription page
            self.driver.get("https://smoothmaths.co.uk/register/11-plus-subscription-plan/")
            print("Navigating to the subscription page")
            
            # Capture screenshot after loading the page
            self.capture_screenshot("subscription_page_loaded")

            # Fill in the form fields using XPath
            self.driver.find_element(By.XPATH, '//*[@id="mepr-address-one"]').send_keys("Muslim road")
            self.driver.find_element(By.XPATH, '//*[@id="mepr-address-city"]').send_keys("Lahore")
            country_dropdown = self.driver.find_element(By.XPATH, '//*[@id="mepr-address-country"]')
            country_dropdown.find_element(By.XPATH, "//option[. = 'Pakistan']").click()
            self.driver.find_element(By.XPATH, '//*[@id="mepr_full_name1"]').send_keys(f"test{random_number}")
            self.driver.find_element(By.XPATH, '//*[@name="mepr-address-state"]').send_keys("Punjab")
            self.driver.find_element(By.XPATH, '//*[@id="mepr-address-zip"]').send_keys("590000")
            self.driver.find_element(By.XPATH, '//*[@id="user_email1"]').send_keys(random_email)
            self.driver.find_element(By.XPATH, '//*[@id="mepr_user_password1"]').send_keys("Hanzila*183258")
            self.driver.find_element(By.XPATH, '//*[@id="mepr_user_password_confirm1"]').send_keys("Hanzila*183258")

            # Scroll down to make the iframe visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Switch to the Stripe iframe for card number input
            stripe_iframes = self.driver.find_elements(By.CSS_SELECTOR, 'iframe[name^="__privateStripeFrame"]')

            # Switch to the card number iframe and fill it
            self.driver.switch_to.frame(stripe_iframes[0])
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#Field-numberInput')))
            self.driver.find_element(By.CSS_SELECTOR, '#Field-numberInput').send_keys("4649 5102 1304 1970")

            # Switch to the expiry date iframe and fill it
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(stripe_iframes[1])
            self.driver.find_element(By.CSS_SELECTOR, '#Field-expiryInput').send_keys("08 / 27")

            # Switch to the CVC iframe and fill it
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(stripe_iframes[2])
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#Field-cvcInput')))
            self.driver.find_element(By.CSS_SELECTOR, '#Field-cvcInput').send_keys("885")

            # Switch back to the main content after card details are filled
            self.driver.switch_to.default_content()

            # Now fill in the additional fields using CSS selectors after card details
            self.driver.find_element(By.CSS_SELECTOR, 'input#Field-linkLegalNameInput').send_keys(f"Test {random_number}")  # Full name field
            self.driver.find_element(By.CSS_SELECTOR, 'input#Field-linkMobilePhoneInput').send_keys("03025265090")  # Phone number field

            # Scroll to the submit button
            register_button = self.driver.find_element(By.XPATH, '//*[@class="mepr-submit"]')
            self.driver.execute_script("arguments[0].scrollIntoView(true);", register_button)

            # Submit the form using XPath
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="mepr-submit"]')))
            register_button.click()

            # Capture screenshot **after** form submission
            self.capture_screenshot("after_form_submission")

            # Wait for 'Thank You' text to appear
            thank_you_text = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Thank you')]"))
            )
            assert "Thank you" in thank_you_text.text
            print("Form submitted successfully, 'Thank You' message found.")

            # Capture screenshot after successful submission
            self.capture_screenshot("thank_you_page")

            status = "Passed"

        except TimeoutException:
            # Handle the exception and save a failure screenshot
            screenshot_path = self.capture_screenshot("subscription_failed")
            print(f"Exception occurred: Timed out waiting for the Thank You message.")

        except NoSuchElementException:
            print("Payment fields not found, check if the iframe is loaded correctly.")

        finally:
            # Save the results in a CSV file
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            self._store_test_results("Subscription Test", status, screenshot_path, duration)
            print(f"Test completed in {duration} seconds.")

    def _store_test_results(self, test_case, status, screenshot_path, duration):
        # Prepare results for CSV
        results = {
            "Test Case": [test_case],
            "Status": [status],
            "Screenshot": [screenshot_path],
            "Duration": [duration]
        }

        # Append results to the CSV file
        if not os.path.exists(CSV_FILE_PATH):
            pd.DataFrame(results).to_csv(CSV_FILE_PATH, index=False)
        else:
            pd.DataFrame(results).to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
