def test_11Plus(self):
    # Start time to calculate test duration
    start_time = time.time()

    # Log in to WordPress
    self.driver.get("https://smoothmaths.co.uk/login/")
    self.driver.find_element(By.ID, "user_login").send_keys("hanzila@dovidigital.com")
    self.driver.find_element(By.ID, "user_pass").send_keys("Hanzila*183258")
    self.driver.find_element(By.ID, "wp-submit").click()
    
    # Open the target page
    self.driver.get("https://smoothmaths.co.uk/11-plus-schools/alleyns-school/")
    
    try:
        # Scroll down a bit after landing on the page
        self.driver.execute_script("window.scrollBy(0, 300);")  # Adjust 300 to scroll by the desired amount
        
        # Click on the "Answer Paper" link
        self.driver.find_element(By.LINK_TEXT, "Answer Paper").click()
        
        # Wait for the first answer paper link to appear and click it
        first_answer_paper = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".et_pb_blurb_4 .et_pb_blurb_container a"))
        )
        first_answer_paper.click()
        
        # Verify the current URL after clicking the answer paper link
        expected_url = "https://smoothmaths.co.uk/11-plus-schools/alleyns-school/allyens-11-maths-sample-examination-paper-1-answer-paper/"
        WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))
        
        # Assert the URL is correct, if not, raise an AssertionError
        assert self.driver.current_url == expected_url, f"Expected URL to be {expected_url}, but got {self.driver.current_url}"
        
        # Capture screenshot
        screenshot_path = "screenshots/First_Paper.png"
        self.driver.save_screenshot(screenshot_path)

        # Set test status to pass
        status = "Pass"

    except Exception as e:
        # Capture any errors
        status = f"Fail: {str(e)}"
        screenshot_path = "screenshots/error_screenshot.png"
        self.driver.save_screenshot(screenshot_path)
    
    # Calculate duration and log results
    end_time = time.time()
    duration = end_time - start_time

    # Prepare results for CSV
    results = {
        "Test Case": ["Test Login and 11+ Paper Navigation"],
        "Status": [status],
        "Duration (seconds)": [round(duration, 2)],
        "Screenshot": [screenshot_path]
    }

    # Append results to the CSV file
    self.append_to_csv(results)
