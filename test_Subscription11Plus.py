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

        # Scroll down to make the iframe visible
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Click the submit button first without filling any additional fields
        register_button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.mepr-submit'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
        self.driver.execute_script("arguments[0].click();", register_button)

        # Wait for the additional fields to appear (e.g., phone number, legal name)
        try:
            # Wait for the additional fields to load (phone number and legal name field)
            additional_fields_loaded = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#Field-linkLegalNameInput'))
            )
            
            # If the fields are present, take the screenshot and fill them out
            if additional_fields_loaded:
                print("Additional fields appeared, waiting for them to load...")
                self.capture_screenshot("additional_fields_loaded")
                
                # Fill in the additional fields
                self.driver.find_element(By.CSS_SELECTOR, 'input#Field-linkLegalNameInput').send_keys(f"Test {random_number}")
                self.driver.find_element(By.CSS_SELECTOR, 'input#Field-linkMobilePhoneInput').send_keys("03012345678")
                
                # Scroll to the submit button and click again
                self.driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
                self.driver.execute_script("arguments[0].click();", register_button)

        except TimeoutException:
            print("No additional fields appeared, proceeding without them.")
        
        # Capture screenshot after form submission
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
