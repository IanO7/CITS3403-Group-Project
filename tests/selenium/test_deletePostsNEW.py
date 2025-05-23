# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestDeletePostsNEW():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_deletePostsNEW(self):
    self.driver.get("http://127.0.0.1:5000/landing")
    self.driver.set_window_size(1550, 926)
    self.driver.find_element(By.LINK_TEXT, "Login").click()
    self.driver.find_element(By.ID, "email-input").click()
    self.driver.find_element(By.ID, "email-input").send_keys("heidi@example.com")
    self.driver.find_element(By.ID, "password-input").send_keys("heidipass")
    self.driver.find_element(By.ID, "password-input").send_keys(Keys.ENTER)
    self.driver.find_element(By.CSS_SELECTOR, ".col:nth-child(1) .btn-outline-danger").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".col:nth-child(1) .btn-outline-danger")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element, 0, 0).perform()
    self.driver.find_element(By.ID, "confirmDeletePostBtn").click()
    self.driver.find_element(By.LINK_TEXT, "Logout").click()
    self.driver.find_element(By.ID, "email-input").click()
    self.driver.find_element(By.ID, "email-input").send_keys("heidi@example.com")
    self.driver.find_element(By.ID, "password-input").send_keys("heidipass")
    self.driver.find_element(By.ID, "password-input").send_keys(Keys.ENTER)
    self.driver.find_element(By.CSS_SELECTOR, ".card").click()
    self.driver.find_element(By.LINK_TEXT, "Logout").click()
    self.driver.find_element(By.LINK_TEXT, "OZfoody").click()
  
