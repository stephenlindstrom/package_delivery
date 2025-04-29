class ChainingHashTable:
  # Constructor with optional initial capacity parameter
  # Creates a list of empty buckets
  def __init__(self, initial_capacity=10):
    self.table = []
    for i in range(initial_capacity):
      self.table.append([])

  # Returns string representation of the hash table
  def __str__(self):
    output = ""
    for i in range(len(self.table)):
      for obj in self.table[i]:
        output += f"{obj}\n"
    return output if output else "Empty Hash Table"

  # Inserts a new object into the hash table
  # Updates the object if an object with the same ID already exists
  # Assumes input is a complete object with an ID attribute
  # Can be refactored to accept separate fields if needed
  def insert(self, obj):
    # Get the bucket list where this object should go.
    bucket_list = self._get_bucket_list(obj.obj_id)

    # Update the object if ID already exists
    for i, item in enumerate(bucket_list):
      if item.obj_id == obj.obj_id:
        bucket_list[i] = obj
        return True
    
    # If ID does not exist, append object to the end of bucket list
    bucket_list.append(obj)
    return True
  
  # Returns the object for the given ID, or None if not found
  def search(self, obj_id):
    # Get the bucket list where this ID should be
    bucket_list = self._get_bucket_list(obj_id)

    # Search for object with matching ID in the bucket list
    for obj in bucket_list:
      if obj.obj_id == obj_id:
        return obj
    return None
  
  # Removes the object with the given ID
  # Returns True if removed or False if not found
  def remove(self, obj_id):
    # Get the bucket list where this ID should be
    bucket_list = self._get_bucket_list(obj_id)

    # Search for object with matching ID and remove it
    for i, obj in enumerate(bucket_list):
      if obj.obj_id == obj_id:
        del bucket_list[i]
        return True
    return False
  
  # Helper method to get the bucket list for a given key
  def _get_bucket_list(self, key):
    bucket = hash(key) % len(self.table)
    return self.table[bucket]

