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

  truck1 = Truck(1, "08:00")
  truck2 = Truck(2, "09:05")
  load_truck(truck1, package_hash_table, distance_matrix, address_list)
  load_truck(truck2, package_hash_table, distance_matrix, address_list)
  deliver_packages(truck1, distance_matrix, address_list)
  deliver_packages(truck2, distance_matrix, address_list)
  # print(truck1.return_time)
  # print(truck2.return_time)
  package9_ready_time = datetime.strptime("10:20", "%H:%M")
  driver_ready_time = min(truck1.return_time, truck2.return_time)
  truck3_departure_time = max(driver_ready_time, package9_ready_time).strftime("%H:%M")
  # print(truck3_departure_time)
  truck3 = Truck(3, truck3_departure_time)
  trucks = [truck1, truck2, truck3]
  load_truck(truck3, package_hash_table, distance_matrix, address_list)
  deliver_packages(truck3, distance_matrix, address_list)
  user_interface(package_hash_table, trucks)
  # print(package_hash_table)
  # print(truck1.distance_traveled + truck2.distance_traveled + truck3.distance_traveled)
  # packages = [bucket_list[0] for bucket_list in package_hash_table.table]
  # print(delivered_on_time(packages))

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
  required_truck_packages = [
    package
    for bucket_list in package_hash_table.table if bucket_list
    for package in bucket_list
    if ( 
        package.delivery_status == "hub" 
        and package.truck_requirement == truck.truck_id 
        and (package.ready_time is None or package.ready_time <= truck.departure_time)
        )
  ]

  non_required_truck_packages = [
    package
    for bucket_list in package_hash_table.table if bucket_list
    for package in bucket_list
    if ( 
        package.delivery_status == "hub" 
        and package.truck_requirement is None
        and (package.ready_time is None or package.ready_time <= truck.departure_time)
        )
  ]

  deadline_packages = sorted([package for package in non_required_truck_packages if package.deadline], key=lambda package: package.deadline)
  eod_packages = [package for package in non_required_truck_packages if package.deadline is None]

  current_address = "4001 South 700 East"

  while len(truck.packages) < truck.capacity and (required_truck_packages or deadline_packages or eod_packages):
    if required_truck_packages:
      nearest_package, _ = find_nearest_package(current_address, required_truck_packages, distance_matrix, address_list)
      truck.packages.append(nearest_package)
      nearest_package.truck_assignment = truck.truck_id
      nearest_package.delivery_status = "in route"
      required_truck_packages.remove(nearest_package)
      current_address = nearest_package.address
    else:
      if deadline_packages:
        nearest_package, _ = find_nearest_package(current_address, deadline_packages, distance_matrix, address_list)
      else:
        nearest_package, _ = find_nearest_package(current_address, eod_packages, distance_matrix, address_list)

      if nearest_package.group_id:
        package_group = [package for package in deadline_packages + eod_packages if package.group_id == nearest_package.group_id]
        if len(package_group) + len(truck.packages) <= truck.capacity:
          for package in package_group:
            truck.packages.append(package)
            package.truck_assignment = truck.truck_id
            package.delivery_status = "in route"
            if package in deadline_packages:
              deadline_packages.remove(package)
            else:
              eod_packages.remove(package)
          current_address = nearest_package.address
        else:
          if nearest_package in deadline_packages:
            deadline_packages.remove(nearest_package)
          else:
            eod_packages.remove(nearest_package)
      else:
        truck.packages.append(nearest_package)
        nearest_package.truck_assignment = truck.truck_id
        nearest_package.delivery_status = "in route"
        if nearest_package in deadline_packages:
          deadline_packages.remove(nearest_package)
        else:
          eod_packages.remove(nearest_package)
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

def user_interface(package_hash_table, trucks):
  while True:
    print("Western Governors University Parcel Service")
    print("1. View Status of All Packages")
    print("2. View Status of a Package")
    print("3. View Truck Mileage")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
      view_all_packages(package_hash_table, trucks)
    elif choice == "2":
      view_package(package_hash_table, trucks)
    elif choice == "3":
      view_truck_mileage(trucks)
    elif choice == "4":
      break
    else:
      print("Invalid input. Please enter 1-4")

def view_all_packages(package_hash_table, trucks):
  while(True):
    print("View Status of All Packages at Given Time")
    user_input = input("Enter a time using 24-hour format (ie 13:52) or 'q' to return to home page: ")
    if user_input.lower() == 'q':
      break
    try:
      time = datetime.strptime(user_input, "%H:%M")
    except ValueError:
      print("Wrong time format")
      continue
    packages = sorted(
      [
        package
        for bucket in package_hash_table.table if bucket
        for package in bucket
      ],
      key=lambda package: package.obj_id
    )

    print(f"{'Package':<10}{'Status':<25}{'Truck':<10}")
    for package in packages:
      assigned_truck = next((t for t in trucks if t.truck_id == package.truck_assignment), None)
      if time < package.delivery_time:
        if assigned_truck is None or time < assigned_truck.departure_time:
              package_status = "At the hub"
              truck_status = "None"
        else: 
          package_status = "In route"
          truck_status = assigned_truck.truck_id
      else:
        delivery_time = package.delivery_time.strftime("%H:%M")
        package_status = f"Delivered at {delivery_time}"
        truck_status = assigned_truck.truck_id

      print(f"{package.obj_id:<10}{package_status:<25}{str(truck_status):<10}")


def view_package(package_hash_table, trucks):
  while(True):
    print("View Status of a Package at Given Time")
    package_input = input("Enter a package number (1-40) or 'q' to return to home page: ")
    if package_input.lower() == 'q':
      break
    try:
      package_number = int(package_input)
    except ValueError:
      print("Invalid input. Not an integer.")
      continue
    if package_number < 1 or package_number > 40:
      print("Invalid input. Not between 1-40")
      continue

    package = package_hash_table.search(package_number)

    if package is None:
      print("Package not found.")
    
    else:
      time_input = input("Enter a time using 24-hour format (ie 13:52) or 'q' to return to home page: ")
      if time_input.lower() == 'q':
        break
      try:
        time = datetime.strptime(time_input, "%H:%M")
      except ValueError:
        print("Wrong time format")
        continue

      print(f"{'Package':<10}{'Status':<25}{'Truck':<10}")
      assigned_truck = next((t for t in trucks if t.truck_id == package.truck_assignment), None)
      if time < package.delivery_time:
        if assigned_truck is None or time < assigned_truck.departure_time:
              package_status = "At the hub"
              truck_status = "None"
        else: 
          package_status = "In route"
          truck_status = assigned_truck.truck_id
      else:
        delivery_time = package.delivery_time.strftime("%H:%M")
        package_status = f"Delivered at {delivery_time}"
        truck_status = assigned_truck.truck_id

      print(f"{package.obj_id:<10}{package_status:<25}{str(truck_status):<10}")

def view_truck_mileage(trucks):
  total_distance = 0
  for truck in trucks:
    total_distance = total_distance + truck.distance_traveled
    print(f"{truck.truck_id}: {truck.distance_traveled:.1f}")
  print(f"Total mileage: {total_distance:.1f}")


if __name__ == "__main__":
  main()