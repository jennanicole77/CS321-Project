from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Selenium Driver is different for the OS you are using, choose one of the following
PATH = "dependencies/windowschromedriver"
#PATH = "dependencies/m1chromedriver"
#PATH = "dependencies/macchromedriver"




# A class that defines the attributes of a GPU
class GPU:
    def __init__(self, name, hash, power):
        self.name = name
        self.hash = hash
        self.power = power
        self.quantity = 0
    def __str__(self):
        return "name: {0}, hash: {1}, power: {2}, quantity: {3}".format(self.name, self.hash, self.power, self.quantity)

# Class that stores the User's parameters
class User:
    def __init__(self, ethereum, ppw, user_gpu):
        self.ethereum = ethereum
        self.ppw = ppw
        self.user_gpu = user_gpu
        self.total_hashrate = self.get_total_hashrate()
        self.roi = 1
    def __str__(self):
        return "amount of ethereum: {0}, price per wattage: {1}, total hashrate: {2}".format(self.ethereum, self.ppw, self.total_hashrate)
    
    # Returns the total hash rate of the user's GPUs
    def get_total_hashrate(self):
        total_hashrate =  0
        for keys in self.user_gpu:
            total_hashrate += float(self.user_gpu[keys].hash) * float(self.user_gpu[keys].quantity)
        return total_hashrate

    # Returns the total cost of power consumption in a 24 hour period
    def  power_usage(self):
        power_usage = 0
        total_gpu_power = 0
        for keys in self.user_gpu:
            total_gpu_power += float(self.user_gpu[keys].power) * float(self.user_gpu[keys].quantity)
        power_usage = (total_gpu_power/1000) * self.ppw * 24
        return power_usage

    # Returns expected daily revenue before power costs
    def daily_revenue(self):
        daily_revenue = (self.get_total_hashrate()/100) * grab_profitability()
        return daily_revenue

    # Returns expected daily earnings with power costs
    def daily_earnings(self):
        return self.daily_revenue() - self.power_usage()

    # Saves session's data into a json file
    def save(self):
        gpus = dict()
        for keys in self.user_gpu:
            gpus[keys] = {"name" : self.user_gpu[keys].name, "quantity" : self.user_gpu[keys].quantity}

        data = {"ethereum" : self.ethereum, "ppw" : self.ppw, "user gpus" : gpus}

        with open("sessions\saved_session.json", "w") as f:
            json.dump(data, f)

    







# Loads up the GPU name, hashrate and power consumption into a dictionary
def load_gpus(gpu_dict):

    f = open("data/gpuhashrate.dat", "r")
    for lines in f:
        temp_list = lines.split()
        gpu_dict[temp_list[0]] = (GPU(temp_list[0], temp_list[1], temp_list[2]))

    f.close()


# Loads a saved user session
def load():
    f = open("sessions\saved_session.json")
    data = json.load(f)

    gpu_dict = dict()
    user_gpu = dict()
    load_gpus(gpu_dict)

    for keys in data["user gpus"]:
        for x in range(0, data["user gpus"][keys]["quantity"]):
            add_gpus(user_gpu, gpu_dict, data["user gpus"][keys]["name"])


    user = User(data["ethereum"], data["ppw"], user_gpu)
    return user

# Calculates the return on investment
def calculateROI():
    return 1

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







#print(grab_profitability())
#print(grab_eth_price())
gpu_dict = dict()
load_gpus(gpu_dict)
#user_gpu = dict()
#add_gpus(user_gpu, gpu_dict, "1080")
#add_gpus(user_gpu, gpu_dict, "1080")
#add_gpus(user_gpu, gpu_dict, "3080")

#remove_gpus(user_gpu, gpu_dict, "3080")
#remove_gpus(user_gpu, gpu_dict, "1080")


user = load()

print(user.power_usage())

print(user.daily_revenue())

print(user.daily_earnings())

print(user)
#remove_gpus(user.user_gpu, gpu_dict, "3080")
user.save()

for keys in user.user_gpu:
    print(user.user_gpu[keys])

