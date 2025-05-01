from datetime import datetime

class Package:
  # Constructor that initializes package with address, deadline, city, zip code, weight, and delivery status
  def __init__(self, obj_id, address, deadline, city, zip_code, weight, delivery_status, truck_requirement, group_id, ready_time):
    self.obj_id = obj_id
    self.address = address
    self.deadline = datetime.strptime(deadline, "%H:%M") if deadline else None
    self.city = city
    self.zip_code = zip_code
    self.weight = weight
    self.delivery_status = delivery_status
    self.truck_requirement = truck_requirement
    self.group_id = group_id
    self.ready_time = datetime.strptime(ready_time, "%H:%M") if ready_time else None
    self.delivery_time = None
    self.truck_assignment = None

  def __str__(self):
    deadline_str = self.deadline.strftime("%H:%M") if self.deadline else "EOD"
    ready_time_str = self.ready_time.strftime("%H:%M") if self.ready_time else None
    delivery_time_str = self.delivery_time.strftime("%H:%M") if self.delivery_time else None
    return f"{self.obj_id}, {self.address}, {deadline_str}, {self.city}, {self.zip_code}, {self.weight}, {self.delivery_status}, {self.truck_requirement}, {self.group_id}, {ready_time_str}, {delivery_time_str}, {self.truck_assignment}"