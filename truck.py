class Truck:

  def __init__(self, truck_id, departure_time):
    self.truck_id = truck_id
    self.departure_time = departure_time
    self.packages = []
    self.speed = 18
    self.distance_traveled = 0

  def __str__(self):
    message = ""
    for package in self.packages:
      message += f"{package.obj_id}\n"
    return message