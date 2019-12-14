from collections import defaultdict
import math

with open("./input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

reactions = {}
ore_stuff = {}

for line in lines:
    resources, result = line.split(" => ")
    
    amount, element = result.split(" ")
    amount = int(amount)
    
    rs = {}

    for resource in resources.split(", "):
        am, el = resource.split(" ")
        am = int(am)
        rs[el] = am

    reactions[element] = {
        "amount": amount,
        "resources": rs,
    }

    if "ORE" in rs:
        ore_stuff[element] = {
            "ore_amount": rs["ORE"],
            "result_amount": amount,
        }

def lookup_in_first_order_resource(target_resource, target_amount):
    result = defaultdict(int)
    
    r = reactions[target_resource]
    
    multiplier = target_amount // r["amount"]
    if (target_amount % r["amount"]) > 0:
        multiplier += 1
    
    for resource, amount in r["resources"].items():
        if resource in ore_stuff:
            result[resource] += amount * multiplier
        else:
            xxx = lookup_in_first_order_resource(resource, amount * multiplier)
            for vmi_resource, vmi_amount in xxx.items():
                result[vmi_resource] += vmi_amount

    return result

def lookup_in_ore(target_resource, target_amount):
    xx = ore_stuff[target_resource]
    ore_amount = xx["ore_amount"]
    result_amount = xx["result_amount"]
    multiplier = target_amount // result_amount
    if (target_amount % result_amount) > 0:
        multiplier += 1
    return ore_amount * multiplier

def print_graph():
    for result, vmi in reactions.items():
        for resource in vmi["resources"].keys():
            print(f'"{resource}" -> "{result}"')


from pprint import pprint

# pprint(reactions)
# pprint(ore_stuff)

# fuel_in_first_order = lookup_in_first_order_resource("FUEL", 1) 

# pprint(fuel_in_first_order)

# sum_ore = 0
# for resource, amount in fuel_in_first_order.items():
#     sum_ore += lookup_in_ore(resource, amount)

# print(sum_ore)

# visualize in http://www.webgraphviz.com/
# print_graph()


lab = defaultdict(int)

def add_to_lab(chemical, amount):
    produce_info = reactions[chemical]
    
    multiplier = amount // produce_info["amount"]
    if (amount % produce_info["amount"]) > 0:
        multiplier += 1
    
    for chem, am in produce_info["resources"].items():
        lab[chem] -= am*multiplier
    
    lab[chemical] += produce_info["amount"]*multiplier

add_to_lab("FUEL", 1)

while True:
    negative_keys = list(filter(lambda k: k != "ORE" and lab[k] < 0, lab.keys()))
    if len(negative_keys) == 0:
        break
    chemical_to_add = negative_keys[0]
    add_to_lab(chemical_to_add, abs(lab[chemical_to_add]))

# add_to_lab("A", 1)
# add_to_lab("C", 1)
# add_to_lab("B", 1)

pprint(lab)
print(-lab["ORE"])
