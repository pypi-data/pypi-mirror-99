# coding: utf-8
import os
import time, logging
from seleniumqt.sk2 import gte
import traceback


def run(driver, element, c):
    try:
        cl = ['#5FB878', '#FF5722', '#FFB800']
        if element:
            try:
                tag_name = element.tag_name
                if tag_name in ["select", "em", "textarea", "input"]: return
                if tag_name == 'button':
                    if element.text == '查询': return
                width = element.rect['width']
                type = element.get_attribute("type")
            except:
                return

            if (type != 'submit' and tag_name == 'input') or width > 800:
                driver.execute_script("arguments[0].setAttribute('style',arguments[1]);",
                                      element, "color:" + cl[c] + " ;")
            else:
                driver.execute_script("arguments[0].setAttribute('style',arguments[1]);",
                                      element, "background:" + cl[c] + " ;")
    except:
        return
