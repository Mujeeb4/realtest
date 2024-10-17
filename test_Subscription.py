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


class Subscription():

    # Subscription Test Function
    def subscribe_paid_plan(self, email, password):
        self.driver.get('https://smoothmaths.co.uk/register/11-plus-subscription-plan/')
        
        # Fill out the subscription form
        email_field = self.driver.find_element(By.NAME, 'email')
        password_field = self.driver.find_element(By.NAME, 'password')
        confirm_password_field = self.driver.find_element(By.NAME, 'password_confirmation')

        email_field.send_keys(hanzilarafiq2@gmail.com)
        password_field.send_keys(Hanzila*183258)
        confirm_password_field.send_keys(Hanzila*183258)

        # Simulate the register button click
        register_button = self.driver.find_element(By.ID, 'register-button')
        register_button.click()
        
        time.sleep(3)

        self.save_screenshot('subscription_free')

        # Fill in Stripe test payment details (Stripe Test Mode)
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//iframe[@title='Secure card number input frame']"))
        card_number_input = self.driver.find_element(By.NAME, 'cardnumber')
        card_number_input.send_keys('4242424242424242')  # Test card number
        
        self.driver.switch_to.default_content()

        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//iframe[@title='Secure expiration date input frame']"))
        expiry_date_input = self.driver.find_element(By.NAME, 'exp-date')
        expiry_date_input.send_keys('12/34')  # Future expiry date

        self.driver.switch_to.default_content()

        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//iframe[@title='Secure CVC input frame']"))
        cvc_input = self.driver.find_element(By.NAME, 'cvc')
        cvc_input.send_keys('123')  # Valid 3-digit CVC code

        self.driver.switch_to.default_content()

        # Click the Pay/Subscribe button
        pay_button = self.driver.find_element(By.ID, 'pay-button')  # Adjust selector if necessary
        pay_button.click()

        time.sleep(3)

        self.save_screenshot('payment_success')

        # Check for success message
        try:
            success_msg = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Thank you for subscribing')]")
            status = "Success" if success_msg.is_displayed() else "Failure"
        except:
            status = "Failure"

        # Log results to a CSV file
        self.append_to_csv([{"Task": "Paid Subscription with Test Payment", "Status": status, "Screenshot": "subscription_free.png", "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}])

    def append_to_csv(self, data, filename="test_results.csv"):
        if not os.path.exists(filename):
            df = pd.DataFrame(columns=["Task", "Status", "Screenshot", "Timestamp"])
            df.to_csv(filename, index=False)
        
        df = pd.read_csv(filename)
        new_data = pd.DataFrame(data)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(filename, index=False)

# pytest function for running the test
def test_subscription():
    subscription_test = Subscription()
    subscription_test.setup_method()
    try:
        subscription_test.subscribe_paid_plan("dummy_user@example.com", "TestPassword123")
    finally:
        subscription_test.teardown_method()
