from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

DELAY = 0.2


def click_button_by_id(css_id):
    driver.find_element(By.ID, css_id).click()
    time.sleep(DELAY)

def drag_drop_to_location(css_id, x, y):
    elem = driver.find_element(By.ID, css_id)
    start_pos = elem.location
    x -= start_pos["x"]
    y -= start_pos["y"]
    action = ActionChains(driver)
    action.drag_and_drop_by_offset(elem, x, y).perform()
    time.sleep(DELAY)

PYSOM_URL = "http://localhost:1234/"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

time.sleep(1)

driver.get(PYSOM_URL)

print(driver.title)

click_button_by_id("view-btn")
click_button_by_id("menu-editor")

input_node_id = "ddn_1"
output_node_id = "ddn_2"

input_node_btn_id = "ddn_add_1"
output_node_btn_id = "ddn_add_2"

drag_drop_to_location(input_node_id, 250, 150)
drag_drop_to_location(output_node_id, 1750, 950)

for i in range(3,15):
    click_button_by_id("add-node-btn")
    click_button_by_id("single-som-btn")

    click_button_by_id("add-link-btn")
    click_button_by_id(input_node_btn_id)
    click_button_by_id(f"ddn_add_{i}")

    click_button_by_id("add-link-btn")
    click_button_by_id(f"ddn_add_{i}")
    click_button_by_id(output_node_btn_id)

    drag_drop_to_location(f"ddn_{i}", 150 * i, 500)
