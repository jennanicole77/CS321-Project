from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



# A class that defines the attributes of a GPU
class GPU:
    def __init__(self, name, hash, power):
        self.name = name
        self.hash = hash
        self.power = power
        self.quantity = 0
    def __str__(self):
        return "name: {0}, hash: {1}, power: {2}, quantity: {3}".format(self.name, self.hash, self.power, self.quantity)

# Loads up the GPU name, hashrate and power consumption into a dictionary. 
def load_gpus(gpu_dict):

    f = open("data/gpuhashrate.dat", "r")
    for lines in f:
        temp_list = lines.split()
        gpu_dict[temp_list[0]] = (GPU(temp_list[0], temp_list[1], temp_list[2]))

    f.close()

# This function adds a gpu to the user dictionary
def add_gpus(user_gpu, gpu_dict, name):
    
    user_gpu[gpu_dict[name].name] = gpu_dict[name]
    user_gpu[name].quantity = user_gpu[name].quantity + 1

# This function removes a gpu from the user dictionary
def remove_gpus(user_gpu, gpu_dict, name):
    
    if name in user_gpu.keys():
        if user_gpu[name].quantity == 1:
            user_gpu.pop(name)
        else:
            user_gpu[name].quantity = user_gpu[name].quantity - 1

# This function grabs the profitablility per 100Mhs of ethereum
def grab_profitability():

    # Url where profitability will be pulled from
    hiveon_url = "https://hiveon.net/"

    PATH = "dependencies/m1chromedriver"

    #Forces selenium to run on headless mode
    op = webdriver.ChromeOptions()
    op.add_argument('headless')

    # Loads up the webdriver and page
    driver = webdriver.Chrome(PATH, options=op)
    #driver = webdriver.Chrome(PATH)
    driver.get(hiveon_url)
    


    #Finds the required value on the website and pulls the information 
    location = "/html/body/div[1]/div[1]/div/section[3]/div/div/div[1]/div[2]"
    try:
        main = WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.XPATH, location), ".")
    )
    finally:
        price_string = driver.find_element_by_xpath(location).text
        driver.quit()
    
    # Parses the return string

    price_string = price_string.replace('$', ' ')
    split_string = price_string.split()

    float_price = float(split_string[0])

    return float_price

# This function grabs the Price of a single
def grab_eth_price():
    # Url where profitability will be pulled from
    url = "https://www.google.com/search?q=Ethereum+Price&oq=Ethereum+Price&aqs=chrome..69i57j69i60.1759j0j4&sourceid=chrome&ie=UTF-8"

    PATH = "dependencies/m1chromedriver"

    #Forces selenium to run on headless mode
    op = webdriver.ChromeOptions()
    op.add_argument('headless')

    # Loads up the webdriver and page
    driver = webdriver.Chrome(PATH, options=op)
    driver.get(url)
    
    #Finds the required value on the website and pulls the information 
    location = "/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div[1]/div/div[1]/div[1]/div[2]/span[1]"
    price_string = driver.find_element_by_xpath(location).text
    price_string = price_string.replace(',', '')
    
    float_price = float(price_string)

    return float_price







print(grab_profitability())
print(grab_eth_price())
gpu_dict = dict()
load_gpus(gpu_dict)
user_gpu = dict()
add_gpus(user_gpu, gpu_dict, "1080")
add_gpus(user_gpu, gpu_dict, "1080")
add_gpus(user_gpu, gpu_dict, "3080")

remove_gpus(user_gpu, gpu_dict, "3080")
remove_gpus(user_gpu, gpu_dict, "1080")






for keys in user_gpu:
    print(user_gpu[keys])

