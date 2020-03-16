#!/usr/bin/env python3
import os
import argparse

import yaml
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from contextlib import suppress


class Breitenbach():
    CONFIG_YAML = os.path.join(os.environ['HOME'], '.breitenbach.yaml')

    def __init__(self):
        with open(self.CONFIG_YAML) as f:
            self.config = yaml.full_load(f)

        self.driver = webdriver.Firefox()
        # self.driver.implicitly_wait(5)
        self.actions = ActionChains(self.driver)

    def login(self):
        # load login
        self.driver.get(self.config['login_url'])
        assert "BSC - Breitenbach Software Client" in self.driver.title
        # login
        elem = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "user")))
        elem.clear()
        elem.send_keys(self.config['username'])
        elem = self.driver.find_element_by_id("pass")
        elem.clear()
        elem.send_keys(self.config['password'])
        elem.send_keys(Keys.RETURN) # or ok-button

    def to_workflow(self):
        # to "workflow zentrale"
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, "#gwt-uid-2 > div:nth-child(1)"))).click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        #driver.execute_script('a = document.querySelector("[aria-label=Buchung]");'
        #                      'a.dispatchEvent(new CustomEvent("mousedown"));'
        #                      'a.dispatchEvent(new CustomEvent("mouseup"))')

    def to_booking(self):
        # "buchung" page
        elem = WebDriverWait(self.driver, 5).until(
             expected_conditions.visibility_of_element_located(
                 (By.CSS_SELECTOR,
                  "[aria-label='Buchung']")))
        assert elem
        self.actions.move_to_element(elem).click_and_hold().release().perform()

    def checkin(self):
        #  wait for switched view
        WebDriverWait(self.driver, 5).until(
             expected_conditions.element_to_be_clickable(
                 (By.CSS_SELECTOR,
                  "[aria-label='Kommen']")))

        # avoid deadlock when clicking already selected thing
        with suppress(NoSuchElementException):
            elem = self.driver.find_element_by_css_selector(
                "[aria-label=Kommen][aria-pressed=false]")
            self.actions.move_to_element(
                elem).click_and_hold().release().perform()

        WebDriverWait(self.driver, 5).until(
             expected_conditions.element_to_be_clickable(
                 (By.CSS_SELECTOR,
                  "[aria-label='Kommen'][aria-pressed=true]")))

        elem = self.driver.find_element_by_css_selector(
            "[aria-label='Jetzt Buchen']")
        assert elem
        self.actions.move_to_element(
            elem).click_and_hold().release().perform()

    def checkout(self):
        #  wait for switched view
        WebDriverWait(self.driver, 5).until(
             expected_conditions.element_to_be_clickable(
                 (By.CSS_SELECTOR,
                  "[aria-label='Gehen']")))

        # avoid deadlock when clicking already selected thing
        with suppress(NoSuchElementException):
            elem = self.driver.find_element_by_css_selector(
                "[aria-label=Gehen][aria-pressed=false]")
            self.actions.move_to_element(
                elem).click_and_hold().release().perform()

        elem = self.driver.find_element_by_css_selector(
            "[aria-label=Gehen][aria-pressed=true]")
        assert elem

        elem = WebDriverWait(self.driver, 5).until(
             expected_conditions.element_to_be_clickable(
                 (By.CSS_SELECTOR, "[aria-label='Jetzt Buchen']")))

        assert elem
        self.actions.move_to_element(
            elem).click_and_hold().release().perform()


def main():
    parser = argparse.ArgumentParser(
        description='Breitenbach CLI.')

    parser.add_argument('--checkin', dest='checkin', action='store_true',
                        help='Check in')
    parser.add_argument('--checkout', dest='checkout', action='store_true',
                        help='Check out')

    args = parser.parse_args()

    if args.checkin:
        b = Breitenbach()
        b.login()
        b.to_workflow()
        b.to_booking()
        b.checkin()
    elif args.checkout:
        b = Breitenbach()
        b.login()
        b.to_workflow()
        b.to_booking()
        b.checkout()


if __name__ == '__main__':
    main()
