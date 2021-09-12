import unittest
import inspect
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

'''
class Template(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def testAddSom(self):
        self.browser.get(sys.argv[1])

    def tearDown(self):
        self.browser.quit()
'''

class TestTitle(unittest.TestCase):

    def setUp(self):
        if url[1]:
            self.browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                            desired_capabilities=DesiredCapabilities.CHROME)
        else:
            self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def testTitle(self):
        self.browser.get(url[0])
        self.assertEqual("SOM Web Application",self.browser.title)

    def tearDown(self):
        self.browser.quit()

class TestGraphInterface(unittest.TestCase):

    def setUp(self):
        if url[1]:
            self.browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                            desired_capabilities=DesiredCapabilities.CHROME)
        else:
            self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def testAddSom(self):
        self.browser.get(url[0])

        add = self.browser.find_element_by_id("add-button")
        add.click()
        nodes = self.browser.find_elements_by_class_name("draggable")
        self.assertEqual(len(nodes),3)

    def testAddSomMany(self):
        self.browser.get(url[0])

        add = self.browser.find_element_by_id("add-button")
        for i in range(0,10):
            add.click()
        nodes = self.browser.find_elements_by_class_name("draggable")
        self.assertEqual(len(nodes),12)


    def testDeleteNodeOne(self):
        self.browser.get(url[0])

        add = self.browser.find_element_by_id("add-button")
        add.click()
        nodes = self.browser.find_elements_by_class_name("draggable")
        somnodes = [node for node in nodes if not (node.get_attribute("id") == "input-node" or node.get_attribute("id")=="output-node")]

        for node in somnodes:
            ActionChains(self.browser).key_down(Keys.CONTROL).click(node).key_up(Keys.CONTROL).perform()
            time.sleep(0.1)
        nodes = self.browser.find_elements_by_class_name("draggable")
        self.assertEqual(len(nodes),2)

    def testDeleteNodeSome(self):
        self.browser.get(url[0])

        add = self.browser.find_element_by_id("add-button")
        for i in range(0,10):
            add.click()
        nodes = self.browser.find_elements_by_class_name("draggable")
        for c,node in enumerate(nodes,0):
            ActionChains(self.browser).key_down(Keys.CONTROL).click(node).key_up(Keys.CONTROL).perform()
            time.sleep(0.1)
            if c == 5:
                break
        nodes = self.browser.find_elements_by_class_name("draggable")
        self.assertEqual(len(nodes),7)

    def tearDown(self):
        self.browser.quit()

class IntegTest1(unittest.TestCase):
    
    def setUp(self):
        if url[1]:
            self.browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                            desired_capabilities=DesiredCapabilities.CHROME)
        else:
            self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def testBuildSom(self):
        self.browser.get(url[0])
        upload = self.browser.find_element_by_id("user_file").send_keys(os.getcwd()+"/testing_items/7balls.txt")
        build = self.browser.find_element_by_id("sub_som")
        build.click()
        time.sleep(10)
        iframes = self.browser.find_elements_by_tag_name("iframe")
        self.assertEqual(1,len(iframes)) 

    def testBuild2Soms(self):
        self.browser.get(url[0])
        upload = self.browser.find_element_by_id("user_file").send_keys(os.getcwd()+"/testing_items/7balls.txt")
        build = self.browser.find_element_by_id("sub_som")
        build.click()
        build.click()
        time.sleep(10)
        iframes = self.browser.find_elements_by_tag_name("iframe")
        self.assertEqual(2,len(iframes))

    def testBuildSomMoreIter(self):
        self.browser.get(url[0])
        upload = self.browser.find_element_by_id("user_file").send_keys(os.getcwd()+"/testing_items/7balls.txt")
        iters = self.browser.find_element_by_id("iters").send_keys("50")
        build = self.browser.find_element_by_id("sub_som")
        build.click()
        time.sleep(10)
        iframes = self.browser.find_elements_by_tag_name("iframe")
        self.assertEqual(1,len(iframes)) 


    def tearDown(self):
        self.browser.quit()
        
if __name__ == "__main__":
    url = [sys.argv.pop()]
    if (len(sys.argv) > 1):
        url.append(True)
        sys.argv.pop()
    unittest.main()