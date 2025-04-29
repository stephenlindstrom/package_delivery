class Package:
  # Constructor that initializes package with address, deadline, city, zip code, weight, and delivery status
  def __init__(self, obj_id, address, deadline, city, zip_code, weight, delivery_status):
    self.obj_id = obj_id
    self.address = address
    self.deadline = deadline
    self.city = city
    self.zip_code = zip_code
    self.weight = weight
    self.delivery_status = delivery_status

  def __str__(self):
    return f"{self.obj_id}, {self.address}, {self.deadline}, {self.city}, {self.zip_code}, {self.weight}, {self.delivery_status}"