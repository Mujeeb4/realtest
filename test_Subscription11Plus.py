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

        # Switch to the Stripe iframe using XPath
        stripe_iframe = WebDriverWait(self.driver, 30).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@title="Secure card number input frame"]'))
        )

        # Fill in the payment details using XPath
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//input[@name="cardnumber"]')))
        self.driver.find_element(By.XPATH, '//input[@name="cardnumber"]').send_keys("4242 4242 4242 4242")
        self.driver.find_element(By.XPATH, '//input[@name="exp-date"]').send_keys("08 / 27")
        self.driver.find_element(By.XPATH, '//input[@name="cvc"]').send_keys("885")

        # Switch back to main content
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
