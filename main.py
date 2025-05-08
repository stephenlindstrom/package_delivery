"""
Stephen Lindstrom
ID 012464573
"""
import data_loader

from datetime import datetime, timedelta
from truck import Truck

def main():
  # Load package, distance, and address data from CSV files
  package_hash_table = data_loader.load_package_data("packages.csv")
  distance_matrix = data_loader.load_distance_data("distances.csv")
  address_list = data_loader.load_address_data("addresses.csv")

  # Create truck 1 and truck 2 with departure times of 8:00am and 9:05am, respectively
  # 9:05am departure time for truck 2 allows delayed packages to be loaded on this truck
  truck1 = Truck(1, "08:00")
  truck2 = Truck(2, "09:05")

  # Load and deliver packages in truck 1 and truck 2
  load_truck(truck1, package_hash_table, distance_matrix, address_list)
  load_truck(truck2, package_hash_table, distance_matrix, address_list)
  deliver_packages(truck1, distance_matrix, address_list)
  deliver_packages(truck2, distance_matrix, address_list)
  
  # Truck 3 cannot depart until driver from truck 1 or truck 2 returns
  driver_ready_time = min(truck1.return_time, truck2.return_time)
  # Also, holding truck 3 until at least 10:20am so address of package 9 is known
  package9_ready_time = datetime.strptime("10:20", "%H:%M")
  # Create truck 3 with a departure time set to the later of the driver return time and package 9's ready time  
  truck3_departure_time = max(driver_ready_time, package9_ready_time).strftime("%H:%M")
  truck3 = Truck(3, truck3_departure_time)

  # Correct address of package 9 as truck 3 will not leave until 10:20am at the earliest
  package9 = package_hash_table.search(9)
  package9.address = "410 S State St"
  package9.zip_code = "84111"

  # Load and deliver packages in truck 3
  load_truck(truck3, package_hash_table, distance_matrix, address_list)
  deliver_packages(truck3, distance_matrix, address_list)

  # Display user interface that provides package tracking info
  trucks = [truck1, truck2, truck3]
  user_interface(package_hash_table, trucks)


def distance_between_addresses(address1, address2, distance_matrix, address_list):
  """
  Returns the distance (as a float) between the two provided addresses using the distance matrix
  Raises ValueError if either address is not found in the address list
  """
  try:
    index1 = address_list.index(address1)
    index2 = address_list.index(address2)
    return distance_matrix[index1][index2]
  except ValueError:
    raise ValueError(f"One of the addresses '{address1}' or '{address2}' was not found in the address list.")

 
def find_nearest_package(current_address, packages, distance_matrix, address_list):
  """
  Returns (nearest_package, distance) from current address, or (None, inf) if no packages are provided
  """
  if not packages:
    return (None, float('inf'))
  
  min_distance = float('inf')
  nearest_package = None
  for package in packages:
    distance = distance_between_addresses(current_address, package.address, distance_matrix, address_list)
    if (distance < min_distance):
      min_distance = distance
      nearest_package = package
  return (nearest_package, min_distance)


def load_truck(truck, package_hash_table, distance_matrix, address_list):
  """
  Loads a truck with packages based on priority:
  1. Required truck assignments
  2. Delivery deadlines (earliest first)
  3. End-of-day packages if space remains

  Packages must be at the hub and ready at the truck's departure time
  """
  # Get list of packages that are at the hub, must be on given truck, and are ready to be loaded
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

  # Get list of packages that are at the hub, don't have a required truck, and are ready to be loaded
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

  # Split packages that are not required to be on this truck into those with deadlines and those without
  # Sort packages with deadlines based on deadline time (earliest first)
  deadline_packages = sorted([package for package in non_required_truck_packages if package.deadline], key=lambda package: package.deadline)
  eod_packages = [package for package in non_required_truck_packages if package.deadline is None]

  current_address = "4001 South 700 East"

  # While the truck has room for more packages and more loadable packages remain, continue loading
  while len(truck.packages) < truck.capacity and (required_truck_packages or deadline_packages or eod_packages):
    # Load packages that must be on this truck first
    if required_truck_packages:
      # Get next nearest package to current address from list of required packages 
      nearest_package, _ = find_nearest_package(current_address, required_truck_packages, distance_matrix, address_list)
      truck.packages.append(nearest_package)
      nearest_package.truck_assignment = truck.truck_id
      nearest_package.delivery_status = "in route"
      required_truck_packages.remove(nearest_package)
      # Change current address to address of the loaded package
      current_address = nearest_package.address
    
    # When all required packages are loaded, load non-required packages, starting with those with deadlines
    else:
      if deadline_packages:
        nearest_package, _ = find_nearest_package(current_address, deadline_packages, distance_matrix, address_list)
      else:
        nearest_package, _ = find_nearest_package(current_address, eod_packages, distance_matrix, address_list)
      
      # If a chosen package belongs to a group, load all packages in that group if they fit
      # Otherwise, remove this package from the list it belongs to, and continue with the next nearest package in the next loop iteration
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
      # If a chosen package does not belong to a group, load it and change current address to this package's address
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
  """
  Delivers packages from the given truck using the nearest neighbor algorithm.
  
  Calculates the total distance traveled and records the delivery time for each package 
  based on the truck's speed (18mph). Updates the delivery status and sets the truck's
  return time once all packages are delivered.
  """
  current_address = "4001 South 700 East"
  current_time = truck.departure_time
  truck.distance_traveled = 0

  # Continues delivering packages while there are still packages on the truck 
  while(truck.packages):
    nearest_package, distance = find_nearest_package(current_address, truck.packages, distance_matrix, address_list)
    truck.packages.remove(nearest_package)
    truck.distance_traveled += distance
    # Time of package delivery is calculated by adding time it took to travel the distance to the next address to current time
    current_time += timedelta(seconds=((distance/truck.speed)*3600))
    nearest_package.delivery_time = current_time
    nearest_package.delivery_status = "delivered"
    # Current address is updated so that next time through loop nearest package will be determined based on new address
    current_address = nearest_package.address

  # Return distance and time to hub is calculated and added to distance traveled and current time, respectively  
  distance_to_hub = distance_between_addresses(current_address, "4001 South 700 East", distance_matrix, address_list)
  truck.distance_traveled += distance_to_hub
  current_time += timedelta(seconds=((distance_to_hub/truck.speed)*3600))
  truck.return_time = current_time


def user_interface(package_hash_table, trucks):
  """
  Provides interface so user can:
  1. view status of all packages at a specified time
  2. view status of an identified package at a specified time
  3. view the mileage traveled by each truck and combined mileage 
  """
  # Loops continuosly until the user chooses to exit
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
    # Exits user interface if user enters '4'
    elif choice == "4":
      break
    else:
      print("Invalid input. Please enter 1-4")

def view_all_packages(package_hash_table, trucks):
  # Loops continuously until the user chooses to quit
  while(True):
    print("View Status of All Packages at Given Time")
    user_input = input("Enter a time using 24-hour format (ie 13:52) or 'q' to return to home page: ")
    # Exits the view if user enters 'q' or 'Q'
    if user_input.lower() == 'q':
      break

    # Converts the user input into a datetime object, handles invalid format
    try:
      query_time = datetime.strptime(user_input, "%H:%M")
    except ValueError:
      print("Wrong time format")
      continue

    # Flattens and sorts all packages from the hash table by package ID
    packages = sorted(
      [
        package
        for bucket in package_hash_table.table if bucket
        for package in bucket
      ],
      key=lambda package: package.obj_id
    )

    # Prints column headers with formatting
    print(f"{'Package':<10}{'Address':<45}{'City':<25}{'Zip Code':<10}{'Weight (kg)':<15}{'Status':<35}{'Deadline':<10}{'Truck':<10}")
    for package in packages:
      address = package.address
      zip_code = package.zip_code
      # Display incorrect address for package 9 prior to 10:20am
      if package.obj_id == 9:
        if query_time < package.ready_time:
          address = "300 State St" 
          zip_code = "84103"

      # Finds the truck that the package is assigned to, if any
      assigned_truck = next((t for t in trucks if t.truck_id == package.truck_assignment), None)

      # If package has not yet been delivered
      if not package.delivery_time or query_time < package.delivery_time:
        # If package isn't assigned to a truck or truck has not left yet
        if assigned_truck is None or query_time < assigned_truck.departure_time:
              package_status = "At the hub"
              truck_status = "None"
        else: 
          package_status = "In route"
          truck_status = assigned_truck.truck_id
      else:
        # If package has been delivered, formats delivery time and determines if it was on time
        delivery_time = package.delivery_time.strftime("%H:%M")
        package_status = f"Delivered at {delivery_time}"
        truck_status = assigned_truck.truck_id
        if package.deadline and package.delivery_time > package.deadline:
          package_status += " Late"
        else: 
          package_status += " On time"

      # Formats deadline for display
      if package.deadline:
        deadline = package.deadline.strftime("%H:%M")
      else:
        deadline = "EOD"

      # Prints package info in respective columns
      print(f"{package.obj_id:<10}{address:<45}{package.city:<25}{zip_code:<10}{package.weight:<15}{package_status:<35}{deadline:<10}{str(truck_status):<10}")


def view_package(package_hash_table, trucks):
  # Loops continuously until the user chooses to quit
  while(True):
    print("View Status of a Package at Given Time")
    package_input = input("Enter a package number (1-40) or 'q' to return to home page: ")

    # Exits the view if user enters 'q' or 'Q'
    if package_input.lower() == 'q':
      break

    # Validates that the input is an integer
    try:
      package_number = int(package_input)
    except ValueError:
      print("Invalid input. Not an integer.")
      continue

    # Ensures package number is within valid range
    if package_number < 1 or package_number > 40:
      print("Invalid input. Not between 1-40")
      continue

    # Searches for the package in the hash table
    package = package_hash_table.search(package_number)

    if package is None:
      print("Package not found.")
    
    else:
      # Prompts user to input a time
      time_input = input("Enter a time using 24-hour format (ie 13:52) or 'q' to return to home page: ")
      if time_input.lower() == 'q':
        break

      # Converts time input into a datetime object
      try:
        query_time = datetime.strptime(time_input, "%H:%M")
      except ValueError:
        print("Wrong time format")
        continue
      
      # Prints column headers for display
      print(f"{'Package':<10}{'Address':<45}{'City':<25}{'Zip Code':<10}{'Weight (kg)':<15}{'Status':<35}{'Deadline':<10}{'Truck':<10}")

      address = package.address
      zip_code = package.zip_code

      # Display incorrect address for package 9 prior to 10:20am
      if package.obj_id == 9:
        if query_time < package.ready_time:
          address = "300 State St" 
          zip_code = "84103"

      # Finds the truck that the package is assigned to, if any
      assigned_truck = next((t for t in trucks if t.truck_id == package.truck_assignment), None)

      # Determines package status based on query time
      if query_time < package.delivery_time:
        if assigned_truck is None or query_time < assigned_truck.departure_time:
              package_status = "At the hub"
              truck_status = "None"
        else: 
          package_status = "In route"
          truck_status = assigned_truck.truck_id
      else:
        delivery_time = package.delivery_time.strftime("%H:%M")
        package_status = f"Delivered at {delivery_time}"
        truck_status = assigned_truck.truck_id
        if package.deadline and package.delivery_time > package.deadline:
          package_status += " Late"
        else: 
          package_status += " On time"

      # Formats deadline for display
      if package.deadline:
        deadline = package.deadline.strftime("%H:%M")
      else:
        deadline = "EOD"

      # Prints formatted output for selected package
      print(f"{package.obj_id:<10}{address:<45}{package.city:<25}{zip_code:<10}{package.weight:<15}{package_status:<35}{deadline:<10}{str(truck_status):<10}")

def view_truck_mileage(trucks):
  """
  Prints mileage, departure time, and return time for each truck as well as combined mileage
  """
  total_distance = 0
  print(f"{'Truck':<10}{'Mileage':<10}{'Departure Time':<17}{'Return Time':<15}")
  for truck in trucks:
    departure_time = truck.departure_time.strftime("%H:%M")
    if truck.return_time:
      return_time = truck.return_time.strftime("%H:%M")
    else:
      return_time = "None"
    total_distance = total_distance + truck.distance_traveled
    print(f"{truck.truck_id:<10}{truck.distance_traveled:<10.1f}{departure_time:<17}{return_time:<15}")
  print(f"Total mileage: {total_distance:.1f} miles")


if __name__ == "__main__":
  main()