from datetime import datetime

class Truck:
  # Constructor that initializes truck with given id and departure time
  def __init__(self, truck_id, departure_time):
    self.truck_id = truck_id
    # Converts given departure time to datetime object
    self.departure_time = datetime.strptime(departure_time, "%H:%M")
    self.packages = []
    # All trucks travel at 18mph
    self.speed = 18
    # Mileage initialized to 0
    self.distance_traveled = 0
    # Trucks can carry no more than 16 packages
    self.capacity = 16
    # Return time initialized to None, later to be changed when truck returns to hub
    self.return_time = None