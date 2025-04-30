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

  print(package_hash_table)
  truck1 = Truck(1, "08:00")
  truck2 = Truck(2, "09:05")
  truck3 = Truck(3, "10:05")
  load_truck(truck1, package_hash_table, distance_matrix, address_list)
  load_truck(truck2, package_hash_table, distance_matrix, address_list)
  deliver_packages(truck1, distance_matrix, address_list)
  deliver_packages(truck2, distance_matrix, address_list)
  load_truck(truck3, package_hash_table, distance_matrix, address_list)
  deliver_packages(truck3, distance_matrix, address_list)
  print(package_hash_table)
  print(truck1.distance_traveled)
  print(truck2.distance_traveled)
  print(truck3.distance_traveled)
  packages = [bucket_list[0] for bucket_list in package_hash_table.table]
  print(delivered_on_time(packages))

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
  packages = [
    bucket_list[0] 
    for bucket_list in package_hash_table.table 
    if ( 
        bucket_list
        and bucket_list[0].delivery_status == "hub" 
        and (bucket_list[0].truck_requirement is None or bucket_list[0].truck_requirement == truck.truck_id) 
        and (bucket_list[0].ready_time is None or bucket_list[0].ready_time <= truck.departure_time)
        )
  ]
  current_address = "4001 South 700 East"
  while len(truck.packages) < truck.capacity and packages:
    nearest_package, _ = find_nearest_package(current_address, packages, distance_matrix, address_list)
    if nearest_package.group_id:
      package_group = [package for package in packages if package.group_id == nearest_package.group_id]
      if len(package_group) + len(truck.packages) <= truck.capacity:
        for package in package_group:
          truck.packages.append(package)
          package.delivery_status = "in route"
          packages.remove(package)
        current_address = nearest_package.address
      else:
        packages.remove(nearest_package)
    else:
      truck.packages.append(nearest_package)
      nearest_package.delivery_status = "in route"
      packages.remove(nearest_package)
      current_address = nearest_package.address

def deliver_packages(truck, distance_matrix, address_list):
  current_address = "4001 South 700 East"
  current_time = truck.departure_time
  truck.distance_traveled = 0
  
  while(truck.packages):
    nearest_package, distance = find_nearest_package(current_address, truck.packages, distance_matrix, address_list)
    truck.packages.remove(nearest_package)
    truck.distance_traveled = truck.distance_traveled + distance
    current_time = current_time + timedelta(seconds=((distance/truck.speed)*3600))
    nearest_package.delivery_time = current_time
    nearest_package.delivery_status = "delivered"
    current_address = nearest_package.address
    
  distance_to_hub = distance_between_addresses(current_address, "4001 South 700 East", distance_matrix, address_list)
  truck.distance_traveled = truck.distance_traveled + distance_to_hub
  current_time = current_time + timedelta(seconds=((distance_to_hub/truck.speed)*3600))
  truck.return_time = current_time

def delivered_on_time(packages):
  for package in packages:
    if package.deadline is not None and package.delivery_time > package.deadline:
      return False
  return True


if __name__ == "__main__":
  main()