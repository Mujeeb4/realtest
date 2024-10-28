import pytest
import time
import os
import random
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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

        # Ensure SS directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        yield
        # Save screenshot before quitting the driver
        self.capture_screenshot("final_screenshot")
        self.driver.quit()

    def capture_screenshot(self, name):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.abspath(f"screenshots/{name}_{timestamp}.png")
        if self.driver.save_screenshot(screenshot_path):
            print(f"Screenshot saved successfully: {screenshot_path}")
        else:
            print(f"Failed to save screenshot: {screenshot_path}")
        return screenshot_path

    def solve_hcaptcha(self, site_key, page_url, api_key):
        # Submit hCaptcha challenge to 2Captcha
        captcha_id = requests.post("http://2captcha.com/in.php", data={
            'key': api_key,
            'method': 'hcaptcha',
            'sitekey': site_key,
            'pageurl': page_url
        }).text.split('|')[1]

        # Poll for the solution
        solution_url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}"
        for _ in range(30):
            response = requests.get(solution_url).text
            if 'CAPCHA_NOT_READY' not in response:
                return response.split('|')[1]
            time.sleep(5)

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
            self.driver.find_element(By.XPATH, '//*[@id="mepr_full_name1"]').send_keys(f"Hanzila{random_number}")
            self.driver.find_element(By.XPATH, '//*[@name="mepr-address-state"]').send_keys("Punjab")
            self.driver.find_element(By.XPATH, '//*[@id="mepr-address-zip"]').send_keys("590000")
            self.driver.find_element(By.XPATH, '//*[@id="user_email1"]').send_keys(random_email)
            self.driver.find_element(By.XPATH, '//*[@id="mepr_user_password1"]').send_keys("Hanzila*183258")
            self.driver.find_element(By.XPATH, '//*[@id="mepr_user_password_confirm1"]').send_keys("Hanzila*183258")

            # Scroll down to make the iframe visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Switch to the Stripe iframe for card number input
            stripe_iframe = WebDriverWait(self.driver, 30).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[name^="__privateStripeFrame"]'))
            )

            # Fill in the payment details using CSS selectors from the screenshot
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#Field-numberInput')))
            self.driver.find_element(By.CSS_SELECTOR, '#Field-numberInput').send_keys("4649 5102 1304 1970")
            self.driver.find_element(By.CSS_SELECTOR, '#Field-expiryInput').send_keys("08 / 27")
            self.driver.find_element(By.CSS_SELECTOR, '#Field-cvcInput').send_keys("885")

            # Switch back to the main content after card details are filled
            self.driver.switch_to.default_content()

            # Scroll to the submit button and ensure it is clickable
            register_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.mepr-submit'))
            )

            # Ensure the element is interactable and visible
            self.driver.execute_script("arguments[0].scrollIntoView(true);", register_button)

            # Capture screenshot before form submission
            self.capture_screenshot("before_form_submission")

            # Click the register button
            register_button.click()

            # Check if hCaptcha appears and solve it
            try:
                hcaptcha_frame = WebDriverWait(self.driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[src*="hcaptcha.com"]'))
                )
                print("hCaptcha detected. Attempting to solve...")

                # Replace with your 2Captcha API key and the site key from the hCaptcha
                api_key = "YOUR_2CAPTCHA_API_KEY"
                site_key = "YOUR_HCAPTCHA_SITE_KEY"  # Obtain the site key from the hCaptcha iframe's data-sitekey attribute
                page_url = "https://smoothmaths.co.uk/register/11-plus-subscription-plan/"

                hcaptcha_token = self.solve_hcaptcha(site_key, page_url, api_key)

                # Fill hCaptcha response
                self.driver.execute_script("document.getElementById('h-captcha-response').value = arguments[0];", hcaptcha_token)

                # Switch back to the main content
                self.driver.switch_to.default_content()
                
                # Click the register button again
                register_button.click()

            except TimeoutException:
                print("No hCaptcha detected; proceeding without solving.")

            # Capture screenshot after successful submission
            self.capture_screenshot("Register_Button_Again")

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
