from datetime import datetime

class Truck:
  def __init__(self, truck_id, departure_time):
    self.truck_id = truck_id
    self.departure_time = datetime.strptime(departure_time, "%H:%M")
    self.packages = []
    self.speed = 18
    self.distance_traveled = 0
    self.capacity = 16
    self.return_time = None

  def __str__(self):
    if not self.packages:
      return "No packages loaded"
    message = ""
    for package in self.packages:
      message += f"{package.obj_id}\n"
    return message