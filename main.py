import data_loader

from datetime import datetime, timedelta
from truck import Truck
from package import Package

def main():
  package_hash_table = data_loader.load_package_data("packages.csv")
  distance_matrix = data_loader.load_distance_data("distances.csv")
  address_list = data_loader.load_address_data("addresses.csv")

  # load_truck(truck1, package_hash_table, distance_matrix, address_list)
  # load_truck(truck2, package_hash_table, distance_matrix, address_list)
  # load_truck(truck3, package_hash_table, distance_matrix, address_list)
  # print(truck1)
  # print(truck2)
  # print(truck3)
  # distance = distance_between_addresses("4001 South 700 East", "177 W Price Ave", distance_matrix, address_list)
  # print(distance)
  # print(package_hash_table)

  # truck1 = Truck("08:00")
  # load_truck(truck1, package_hash_table, distance_matrix, address_list)
  # print(package_hash_table)
  # deliver_packages(truck1, distance_matrix, address_list)
  print(package_hash_table)

def distance_between_addresses(address1, address2, distance_matrix, address_list):
  try:
    index1 = address_list.index(address1)
    index2 = address_list.index(address2)
    return distance_matrix[index1][index2]
  except ValueError:
    raise ValueError(f"One of the addresses '{address1}' or '{address2}' was not found in the address list.")
  
def find_nearest_package(current_address, packages, distance_matrix, address_list):
  min_distance = float('inf')
  nearest_package = None
  for package in packages:
    distance = distance_between_addresses(current_address, package.address, distance_matrix, address_list)
    if (distance < min_distance):
      min_distance = distance
      nearest_package = package
  return [nearest_package, min_distance]

def load_truck(truck, package_hash_table, distance_matrix, address_list):
  packages = [bucket_list[0] for bucket_list in package_hash_table.table if bucket_list[0].delivery_status == "hub"]
  current_address = "4001 South 700 East"
  while(len(truck.packages) < 16 and packages):
    nearest_package, _ = find_nearest_package(current_address, packages, distance_matrix, address_list)
    truck.packages.append(nearest_package)
    nearest_package.delivery_status = "in route"
    packages.remove(nearest_package)
    current_address = nearest_package.address

def deliver_packages(truck, distance_matrix, address_list):
  current_address = "4001 South 700 East"
  current_time = datetime.strptime(truck.departure_time, "%H:%M")
  while(truck.packages):
    nearest_package, distance = find_nearest_package(current_address, truck.packages, distance_matrix, address_list)
    truck.packages.remove(nearest_package)
    current_time = current_time + timedelta(seconds=((distance/truck.speed)*3600))
    delivery_time = current_time.strftime("%H:%M")
    nearest_package.delivery_status = f"delivered at {delivery_time}"
    current_address = nearest_package.address




if __name__ == "__main__":
  main()