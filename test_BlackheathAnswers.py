import pytest
import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# CSV file path to store all test results
CSV_FILE_PATH = "test_results.csv"

class TestBlackheathanswers():
    def setup_method(self, method):
        # Set up headless Chrome options for CI
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("window-size=1296,696")
        
        # Set the correct path to ChromeDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.vars = {}
        
        # Ensure screenshots directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
    
    def teardown_method(self, method):
        self.driver.quit()

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        return wh_now

    def append_to_csv(self, results):
        df = pd.DataFrame(results)
        try:
            if os.path.exists(CSV_FILE_PATH):
                df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
            else:
                df.to_csv(CSV_FILE_PATH, mode='w', header=True, index=False)
            print("Successfully appended to CSV.")
        except Exception as e:
            print(f"Error appending to CSV: {e}")

    def test_blackheathanswers(self):
        # Login
        self.driver.get("https://smoothmaths.co.uk/login/")
        self.driver.find_element(By.ID, "user_login").send_keys("hanzila@dovidigital.com")
        self.driver.find_element(By.ID, "user_pass").send_keys("Hanzila*183258")
        self.driver.find_element(By.ID, "wp-submit").click()

        # Open the target page
        self.driver.get("https://smoothmaths.co.uk/11-plus-schools/blackheath-high-school/")
        self.vars["root"] = self.driver.current_window_handle

        # Open the first answer paper in second tab and check the link
        self.driver.find_element(By.CSS_SELECTOR, ".et_pb_blurb_1.et_pb_blurb .et_pb_module_header a").click()
        self.vars["window_handles"] = self.wait_for_window(2000)  # Store window handles after opening the new tab
        self.driver.switch_to.window(self.vars["window_handles"][-1])  # Switch to the newly opened tab

        # Verify the link on the second tab
        second_tab_link = self.driver.current_url
        expected_second_tab_link = "https://smoothmaths.co.uk/blackheath-high-school-11-plus-sample-examination-answer-paper-2024/"
        print(f"Link in second tab: {second_tab_link}")
        
        # Take screenshot of the second tab
        screenshot_path = f"screenshots/second_tab_screenshot.png"
        self.driver.save_screenshot(screenshot_path)

        # Check if the link matches the expected URL
        if second_tab_link != expected_second_tab_link:
            raise Exception(f"Test failed: Expected {expected_second_tab_link} but got {second_tab_link}")

        # Return to the first tab, scroll, and right-click on the second answer paper
        self.driver.switch_to.window(self.vars["root"])
        self.driver.execute_script("window.scrollBy(0, 500)")  # Scroll down 500px
        action = ActionChains(self.driver)
        answer_paper = self.driver.find_element(By.CSS_SELECTOR, ".et_pb_blurb_4.et_pb_blurb .et_pb_module_header a")
        action.context_click(answer_paper).perform()  # Right-click on the second answer paper
        time.sleep(2)  # Wait for the context menu

        # Open the link in a new tab
        action.send_keys(Keys.ARROW_DOWN).send_keys(Keys.RETURN).perform()
        self.vars["window_handles"] = self.wait_for_window(2000)  # Store window handles again after opening the new tab
        self.driver.switch_to.window(self.vars["window_handles"][-1])  # Switch to the new tab

        # Switch to the new tab and check its link
        new_tab_link = self.driver.current_url
        expected_new_tab_link = "https://smoothmaths.co.uk/11-plus-schools/blackheath-high-school/11-entrance-and-scholarship-examination-mathematics-practice-paper-answer-paper/"
        print(f"Link in the new tab after right-click: {new_tab_link}")

        # Check if the link matches the expected URL
        if new_tab_link != expected_new_tab_link:
            raise Exception(f"Test failed: Expected {expected_new_tab_link} but got {new_tab_link}")

        # Close the tabs
        self.driver.close()
        self.driver.switch_to.window(self.vars["root"])

        # Prepare test result
        results = [{
            "Test Case": "Second Tab Link Verification",
            "Status": "Pass",
            "Expected URL": expected_second_tab_link,
            "Actual URL": second_tab_link,
            "Screenshot": screenshot_path
        }]

        # Append results to CSV
        self.append_to_csv(results)
