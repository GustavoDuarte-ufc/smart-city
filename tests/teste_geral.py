from database.database import Database

db = Database()

print(db.get_sensors())
print(db.get_readings())