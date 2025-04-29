import csv

from chaininghashtable import ChainingHashTable
from package import Package

# Loads package data from a CSV file into a given hash table
def load_package_data(filename):
  package_hash_table = ChainingHashTable(40)
  with open(filename) as file:
    package_data = csv.reader(file, delimiter=",")
    for package in package_data:
      obj_id = int(package[0])
      address = package[1]
      city = package[2]
      zip_code = package[3]
      deadline = package[4]
      weight = package[5]
      truck_requirement = int(package[6]) if package[6] else None
      group_id = int(package[7]) if package[7] else None

      pack = Package(obj_id, address, deadline, city, zip_code, weight, "hub", truck_requirement, group_id)
      package_hash_table.insert(pack)
  return package_hash_table

# Load distance data dynamically from a CSV file into a matrix
def load_distance_data(filename):
  distance_data_matrix = []
  with open(filename) as file:
    distance_data = csv.reader(file, delimiter=",")
    for row in distance_data:
      distance_row = [float(distance) for distance in row]
      distance_data_matrix.append(distance_row)
  return distance_data_matrix

# Load addresses from a CSV file into a list
def load_address_data(filename):
  address_list = []
  with open(filename) as file:
    address_data = csv.reader(file, delimiter=",")
    address_list = [row[0] for row in address_data]
  return address_list