import pytest
import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# CSV file path to store test results
CSV_FILE_PATH = "test_results.csv"

@pytest.fixture(autouse=True)
def setup_method():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Ensure screenshots directory exists
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    yield driver
    # Save screenshot before quitting the driver
    capture_screenshot(driver, "final_screenshot")
    driver.quit()

def capture_screenshot(driver, name):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.abspath(f"screenshots/{name}_{timestamp}.png")
    if driver.save_screenshot(screenshot_path):
        print(f"Screenshot saved successfully: {screenshot_path}")
    else:
        print(f"Failed to save screenshot: {screenshot_path}")
    return screenshot_path

def test_subscription(setup_method):
    driver = setup_method
    start_time = time.time()
    status = "Failed"
    screenshot_path = ""
    try:
        # Generate a random email address
        random_number = random.randint(1000, 9999)
        random_email = f"testing{random_number}@gmail.com"

        # Navigate to subscription page
        driver.get("https://smoothmaths.co.uk/register/11-plus-subscription-plan/")
        print("Navigating to the subscription page")
        
        # Capture screenshot after loading the page
        capture_screenshot(driver, "subscription_page_loaded")

        # Scroll down to make the iframe visible
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Click the submit button first without filling any additional fields
        register_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.mepr-submit'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
        driver.execute_script("arguments[0].click();", register_button)

        # Wait for the additional fields to appear (e.g., phone number, legal name)
        try:
            # Wait for the additional fields to load (phone number and legal name field)
            additional_fields_loaded = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#Field-linkLegalNameInput'))
            )
            
            # If the fields are present, take the screenshot and fill them out
            if additional_fields_loaded:
                print("Additional fields appeared, waiting for them to load...")
                capture_screenshot(driver, "additional_fields_loaded")
                
                # Fill in the additional fields
                driver.find_element(By.CSS_SELECTOR, 'input#Field-linkLegalNameInput').send_keys(f"Test {random_number}")
                driver.find_element(By.CSS_SELECTOR, 'input#Field-linkMobilePhoneInput').send_keys("03012345678")
                
                # Scroll to the submit button and click again
                driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
                driver.execute_script("arguments[0].click();", register_button)

        except TimeoutException:
            print("No additional fields appeared, proceeding without them.")
        
        # Capture screenshot after form submission
        capture_screenshot(driver, "after_form_submission")

        # Wait for 'Thank You' text to appear
        thank_you_text = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Thank you')]"))
        )
        assert "Thank you" in thank_you_text.text
        print("Form submitted successfully, 'Thank You' message found.")

        # Capture screenshot after successful submission
        capture_screenshot(driver, "thank_you_page")

        status = "Passed"

    except TimeoutException:
        # Handle the exception and save a failure screenshot
        screenshot_path = capture_screenshot(driver, "subscription_failed")
        print(f"Exception occurred: Timed out waiting for the Thank You message.")

    except NoSuchElementException:
        print("Payment fields not found, check if the iframe is loaded correctly.")

    finally:
        # Save the results in a CSV file
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        _store_test_results("Subscription Test", status, screenshot_path, duration)
        print(f"Test completed in {duration} seconds.")

def _store_test_results(test_case, status, screenshot_path, duration):
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
