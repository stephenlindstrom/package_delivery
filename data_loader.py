import csv

from chaininghashtable import ChainingHashTable
from package import Package

# Returns hash table after loading package data from a CSV file
def load_package_data(filename):
  # Creates hash table with 40 buckets for the 40 packages to limit collisions and improve efficiency
  package_hash_table = ChainingHashTable(40)
  with open(filename) as file:
    package_data = csv.reader(file, delimiter=",")
    # For each line in CSV file (which represents a package), retrieve comma-separated package attributes
    for package in package_data:
      obj_id = int(package[0])
      address = package[1]
      city = package[2]
      zip_code = package[3]
      # "EOD" means "End of Day", so it is stored as None to simplify comparisons
      if package[4] == "EOD":
        deadline = None
      else:
        deadline = package[4]
      weight = package[5]
      # Optional truck_requirement, group_id, and ready_time are set to None if not present
      truck_requirement = int(package[6]) if package[6] else None
      group_id = int(package[7]) if package[7] else None
      ready_time = package[8] if package[8] else None
      # Create Package object using acquired attributes that is inserted into hash table
      # All delivery statuses begin as "hub"
      pack = Package(obj_id, address, deadline, city, zip_code, weight, "hub", truck_requirement, group_id, ready_time)
      package_hash_table.insert(pack)
  return package_hash_table

# Returns matrix after loading distance data from a CSV file
def load_distance_data(filename):
  distance_data_matrix = []
  with open(filename) as file:
    distance_data = csv.reader(file, delimiter=",")
    for row in distance_data:
      # Converts distances from strings to floats, allowing for future computations 
      distance_row = [float(distance) for distance in row]
      distance_data_matrix.append(distance_row)
  return distance_data_matrix

# Returns list of addresses loaded from a CSV file
def load_address_data(filename):
  address_list = []
  with open(filename) as file:
    address_data = csv.reader(file, delimiter=",")
    # Each row in CSV file only has 1 item
    address_list = [row[0] for row in address_data]
  return address_list