from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import math

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
    def __init__(self):
        self.ethereum = 0           #Stores the total amount of ethereum the user has
        self.power_rate = 0         #Stores the power rate of the user in ppw
        self.user_gpu = dict()      #Stores a map that contains all the GPUS the user has
        self.tax_rate = 0           #Stores the percent rate of tax_ratees ex: 0.25
        self.total_cost = 0;        #Stores the money spent with the RIG
        
    def __str__(self):
        return "amount of ethereum: {0}, price per wattage: {1}, total hashrate: {2}, tax_rate: {3}, total_cost: {4}".format(self.ethereum, self.power_rate, self.total_hashrate, self.tax_rate, self.total_cost)
    
    # A constructor used to initialize an user at once when all values are given. 
    def user_constructor(self, ethereum, power_rate, user_gpu, tax_rate, total_cost):
        self.ethereum = ethereum
        self.power_rate = power_rate
        self.user_gpu = user_gpu
        self.tax_rate = tax_rate
        self.total_cost = total_cost

    # Sets the total ammount of ethereum mined, default is 0
    def set_ethereum_mined(self, ethereum):
        self.ethereum = ethereum
    
    # Gets the total amount of ethereum mined
    def get_ethereum_mined(self):
        return self.ethereum
    
    # Sets the total  cost of the system, default is 0
    def set_total_cost(self, total_cost):
        self.total_cost = total_cost
    
    # Gets the total cost of the system
    def get_total_cost(self):
        return self.total_cost
    
     # Sets the total  cost of the system, default is 0
    
    # Sets the tax rate
    def set_tax_rate(self, tax_rate):
        self.tax_rate = tax_rate
    
    # Gets the total cost of the system
    def get_tax_rate(self):
        return self.tax_rate
    
     # Sets the total  cost of the system, default is 0
    
    # Sets the power rate
    def set_power_rate(self, power_rate):
        self.power_rate = power_rate
    
    # Gets the total cost of the system
    def get_power_rate(self):
        return self.power_rate
    
    # Loops through the gpus stored in the user_gpu map adding upthe hashrates of all GPUs
    # Returns the total hash rate of the user's GPUs
    def get_total_hashrate(self):
        total_hashrate =  0
        for keys in self.user_gpu:
            total_hashrate += float(self.user_gpu[keys].hash) * float(self.user_gpu[keys].quantity)
        self.total_hashrate = total_hashrate
        return total_hashrate

    # Loops through the gpus stored in the user_gpu map adding up the power consumption of the Gpus
    # Returns the total cost of power consumption in a 24 hour period
    def  power_usage(self):
        power_usage = 0
        total_gpu_power = 0
        for keys in self.user_gpu:
            total_gpu_power += float(self.user_gpu[keys].power) * float(self.user_gpu[keys].quantity)
        power_usage = (total_gpu_power/1000) * self.power_rate * 24
        return power_usage

    # Returns expected daily revenue before power costs
    # (total_hashrate/100) * (profitabiity per 100Mhs of eth)
    def daily_revenue(self):
        daily_revenue = (self.get_total_hashrate()/100) * grab_profitability()
        return daily_revenue

    # Returns the daily profit adjusted for power and tax_ratees
    def daily_profit(self):
        tax_rate = self.daily_revenue() * self.tax_rate
        daily_profit = self.daily_revenue() -  self.power_usage() - tax_rate
        return daily_profit

    # Saves session's data into a json file
    def save(self):
        gpus = dict()
        for keys in self.user_gpu:
            gpus[keys] = {"name" : self.user_gpu[keys].name, "quantity" : self.user_gpu[keys].quantity}

        data = {"ethereum" : self.ethereum, "power_rate" : self.power_rate, "tax_rate" : self.tax_rate, "total_cost" : self.total_cost, "user gpus" : gpus}

        with open("sessions\saved_session.json", "w") as f:
            json.dump(data, f)
    
    # Loads a saved user session
    def load(self, file):
        f = open("sessions\\" + file)
        data = json.load(f)

        gpu_dict = dict()
        user_gpu = dict()
        load_gpus(gpu_dict)

        for keys in data["user gpus"]:
            for x in range(0, data["user gpus"][keys]["quantity"]):
                self.add_gpus(user_gpu, gpu_dict, data["user gpus"][keys]["name"])

        
        self.user_constructor(data["ethereum"], data["power_rate"], user_gpu, data["tax_rate"], data["total_cost"])
    
    # This function adds a gpu to the user dictionary
    def add_gpus(self, user_gpu, gpu_dict, name):
        user_gpu[gpu_dict[name].name] = gpu_dict[name]
        user_gpu[name].quantity = user_gpu[name].quantity + 1

    # This function removes a gpu from the user dictionary
    def remove_gpus(self, user_gpu, name):
        
        if name in user_gpu.keys():
            if user_gpu[name].quantity == 1:
                user_gpu.pop(name)
            else:
                user_gpu[name].quantity = user_gpu[name].quantity - 1

    # Calculates the return on total_cost
    def calculate_remaining_days_for_ROI(self):

        ROI = self.total_cost/self.daily_profit()
        math.ceil(ROI)
        return str(math.ceil(ROI)) + " days"

        # This function uses selenium to grab the profitablility per 100Mhs of ethereum
    
    #Uses Selenium to grab profitability per 100 Mhs
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

    # This function grabs the Price of a single ETH Coin
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

    
# Loads up the GPU name, hashrate and power consumption into a dictionary
def load_gpus(gpu_dict):

    f = open("data/gpuhashrate.dat", "r")
    for lines in f:
        temp_list = lines.split()
        gpu_dict[temp_list[0]] = (GPU(temp_list[0], temp_list[1], temp_list[2]))

    f.close()

gpu_dict = dict() #A Global variable that stores all the possible GPU Types inside a map
load_gpus(gpu_dict)










user_gpu = dict()
caio = User(0, 1, user_gpu, 0.3, 1000)
caio.set_ethereum_mined(20)

print(caio)




#print(grab_profitability())
#print(grab_eth_price())

#user_gpu = dict()
#add_gpus(user_gpu, gpu_dict, "1080")
#add_gpus(user_gpu, gpu_dict, "1080")
#add_gpus(user_gpu, gpu_dict, "3080")

#remove_gpus(user_gpu, gpu_dict, "3080")
#remove_gpus(user_gpu, gpu_dict, "1080")


#user = load("saved_session.json")

#print("Power usage: " + str(user.power_usage()))

#print("Daily revenue: " + str(user.daily_revenue()))

#print("Daily earnings: " + str(user.daily_profit()))

#print("ROI: " + str(user.calculateROI()))

#print(user)
#remove_gpus(user.user_gpu, gpu_dict, "3080")
#user.save()

#for keys in user.user_gpu:
    #print(user.user_gpu[keys])

