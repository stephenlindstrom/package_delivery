from datetime import datetime

class Package:
  # Constructor that initializes package with id, address, deadline, city, zip code, weight, delivery status, truck requirement, group id, and ready time
  def __init__(self, obj_id, address, deadline, city, zip_code, weight, delivery_status, truck_requirement, group_id, ready_time):
    self.obj_id = obj_id
    self.address = address
    # Converts given deadline to datetime object if present, else set to None
    self.deadline = datetime.strptime(deadline, "%H:%M") if deadline else None
    self.city = city
    self.zip_code = zip_code
    self.weight = weight
    self.delivery_status = delivery_status
    self.truck_requirement = truck_requirement
    self.group_id = group_id
    # Converts given ready time to datetime object if present, else set to None
    self.ready_time = datetime.strptime(ready_time, "%H:%M") if ready_time else None
    # Delivery time and truck assignment are initialized to None, later to be changed when package is loaded and delivered
    self.delivery_time = None
    self.truck_assignment = None

  # Returns string representation of a package
  def __str__(self):
    # Converts deadline, ready time, and delivery time from datetime objects to strings if they exist
    # Deadline is set to "EOD" if it does not exist
    # Ready time and delivery time are set to "N/A" if they do not exist
    deadline_str = self.deadline.strftime("%H:%M") if self.deadline else "EOD"
    ready_time_str = self.ready_time.strftime("%H:%M") if self.ready_time else "N/A"
    delivery_time_str = self.delivery_time.strftime("%H:%M") if self.delivery_time else "N/A"
    return f"{self.obj_id}, {self.address}, {deadline_str}, {self.city}, {self.zip_code}, {self.weight}, {self.delivery_status}, {self.truck_requirement}, {self.group_id}, {ready_time_str}, {delivery_time_str}, {self.truck_assignment}"