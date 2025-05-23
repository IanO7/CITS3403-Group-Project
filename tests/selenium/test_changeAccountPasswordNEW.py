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

class TestChangeAccountPasswordNEW():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_changeAccountPasswordNEW(self):
    self.driver.get("http://127.0.0.1:5000/landing")
    self.driver.set_window_size(1550, 926)
    self.driver.find_element(By.LINK_TEXT, "Login").click()
    self.driver.find_element(By.ID, "email-input").click()
    self.driver.find_element(By.ID, "email-input").send_keys("alice@example.com")
    self.driver.find_element(By.ID, "password-input").send_keys("alicepass")
    self.driver.find_element(By.ID, "eye-icon").click()
    self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(6)").click()
    self.driver.find_element(By.LINK_TEXT, "Settings").click()
    self.driver.find_element(By.ID, "new-password").click()
    self.driver.find_element(By.ID, "eye-icon-new").click()
    self.driver.find_element(By.ID, "confirm-password").click()
    self.driver.find_element(By.ID, "confirm-password").send_keys("Alicepass123!")
    self.driver.find_element(By.ID, "updateBtn").click()
    self.driver.find_element(By.LINK_TEXT, "Logout").click()
    self.driver.find_element(By.ID, "email-input").click()
    self.driver.find_element(By.ID, "email-input").send_keys("alce")
    self.driver.find_element(By.ID, "email-input").send_keys(Keys.DOWN)
    self.driver.find_element(By.ID, "email-input").send_keys("alice@example.com")
    self.driver.find_element(By.ID, "email-input").send_keys(Keys.TAB)
    self.driver.find_element(By.ID, "password-input").send_keys("alicepass")
    self.driver.find_element(By.ID, "eye-icon").click()
    self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(6)").click()
    self.driver.find_element(By.ID, "email-input").click()
    self.driver.find_element(By.ID, "email-input").send_keys("alice")
    self.driver.find_element(By.ID, "email-input").click()
    self.driver.find_element(By.ID, "email-input").send_keys("alice@example.com")
    self.driver.find_element(By.ID, "password-input").send_keys("Alicepass123!")
    self.driver.find_element(By.ID, "eye-icon").click()
    self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(6)").click()
    self.driver.find_element(By.LINK_TEXT, "Logout").click()
    self.driver.find_element(By.LINK_TEXT, "OZfoody").click()
  
