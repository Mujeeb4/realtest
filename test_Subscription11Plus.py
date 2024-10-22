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
            stripe_iframe = WebDriverWait(self.driver, 30).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[name^="__privateStripeFrame"]'))
            )

            # Define the values for the payment fields
            card_number = "4242 4242 4242 4242"
            expiry_date = "08 / 27"
            cvc_code = "885"
            phone_number = "03025265090"  # Updated phone number

            # Fill in the payment details using CSS selectors
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#Field-numberInput')))
            self.driver.find_element(By.CSS_SELECTOR, '#Field-numberInput').send_keys(card_number)
            self.driver.find_element(By.CSS_SELECTOR, '#Field-expiryInput').send_keys(expiry_date)
            self.driver.find_element(By.CSS_SELECTOR, '#Field-cvcInput').send_keys(cvc_code)

            # Switch back to the main content (leave both iframes)
            self.driver.switch_to.default_content()

            # Scroll to the submit button
            register_button = self.driver.find_element(By.XPATH, '//*[@class="mepr-submit"]')
            self.driver.execute_script("arguments[0].scrollIntoView(true);", register_button)

            # Capture screenshot before form submission
            self.capture_screenshot("before_form_submission")

            # Submit the form using XPath
            register_button.click()

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
