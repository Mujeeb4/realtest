import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Subscription():
    def setup_method(self, method):
        # Set up Chrome options for headless execution (suitable for GitHub Actions)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1296, 696)

        # Create a folder for screenshots if it doesn't exist
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def teardown_method(self, method):
        self.driver.quit()

# Subscription Test Function
def subscribe_free_plan(email, password):
    driver.get('https://smoothmaths.co.uk/register/11-plus-subscription-plan/')
    
    # Fill out the subscription form
    email_field = driver.find_element(By.NAME, 'email')
    password_field = driver.find_element(By.NAME, 'password')
    confirm_password_field = driver.find_element(By.NAME, 'password_confirmation')

    email_field.send_keys(hanzilarafiq2@gmail.com)
    password_field.send_keys(Hanzila*183258)
    confirm_password_field.send_keys(Hanzila*183258)

    # Simulate the register button click
    register_button = driver.find_element(By.ID, 'register-button')
    register_button.click()
    
    time.sleep(3)

    save_screenshot('subscription_free')

    # Fill in Stripe test payment details
    driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@title='Secure card number input frame']"))
    card_number_input = driver.find_element(By.NAME, 'cardnumber')
    card_number_input.send_keys('4242424242424242')
    
    driver.switch_to.default_content()

    driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@title='Secure expiration date input frame']"))
    expiry_date_input = driver.find_element(By.NAME, 'exp-date')
    expiry_date_input.send_keys('12/34')

    driver.switch_to.default_content()

    driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@title='Secure CVC input frame']"))
    cvc_input = driver.find_element(By.NAME, 'cvc')
    cvc_input.send_keys('123')

    driver.switch_to.default_content()

    # Click the Pay/Subscribe button
    pay_button = driver.find_element(By.ID, 'pay-button')  # Adjust selector if necessary
    pay_button.click()

    time.sleep(3)

    save_screenshot('payment_success')

    # Check for success message
    try:
        success_msg = driver.find_element(By.XPATH, "//p[contains(text(), 'Thank you for subscribing')]")
        status = "Success" if success_msg.is_displayed() else "Failure"
    except:
        status = "Failure"

    # Log results
    append_to_csv([{"Task": "Free Subscription with Test Payment", "Status": status, "Screenshot": "subscription_free.png", "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}])

# Main Execution
try:
    subscribe_free_plan("dummy_user@example.com", "TestPassword123")
finally:
    zip_screenshots()
    driver.quit()
