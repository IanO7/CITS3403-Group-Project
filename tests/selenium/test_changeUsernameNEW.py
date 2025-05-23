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

class TestChangeUsernameNEW():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_changeUsernameNEW(self):
    self.driver.get("http://127.0.0.1:5000/landing")
    self.driver.set_window_size(1550, 926)
    self.driver.find_element(By.LINK_TEXT, "Login").click()
    self.driver.find_element(By.ID, "email-input").click()
    self.driver.find_element(By.ID, "email-input").send_keys("dan@example.com")
    self.driver.find_element(By.ID, "password-input").send_keys("danpass")
    self.driver.find_element(By.ID, "password-input").send_keys(Keys.ENTER)
    self.driver.find_element(By.LINK_TEXT, "Settings").click()
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("danNEWDAN")
    self.driver.find_element(By.CSS_SELECTOR, "#update-username-form > .btn").click()
    self.driver.find_element(By.LINK_TEXT, "Profile").click()
    self.driver.find_element(By.ID, "profileSub").click()
    self.driver.find_element(By.LINK_TEXT, "Logout").click()
    self.driver.find_element(By.LINK_TEXT, "OZfoody").click()
  
