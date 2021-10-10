
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

