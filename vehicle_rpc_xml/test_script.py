from vehicle_tracking_xmlrpc import VehicleTrackingXMLRPC

# ------------------------------------------
# CONFIGURATION
# ------------------------------------------
url = "http://localhost:8069"
db = "odoo192"      # CHANGE THIS
uid = 2                  # admin UID
password = "123"       # ADMIN PASSWORD

rpc = VehicleTrackingXMLRPC(url)

# ------------------------------------------
# 1️⃣ CREATE NEW RECORD
# ------------------------------------------
new_id = rpc.create(db, uid, password, {
    "vehicle_id": 4,           # Change according to your DB
    "driver_id": 13,          # Change as needed
    "source": "warehouse",
    "destination": "customer_site",
    "start_km": 400,
    "end_km": 500,
    "remarks": "Created via XML-RPC"
})

print("\nCreated Record ID:", new_id)

# ------------------------------------------
# 1.1️⃣ READ THE NEW RECORD (GET REF)
# ------------------------------------------
record = rpc.read_one(db, uid, password, new_id)
print("\nNew Record Details:", record)
print("Generated REF =", record["ref"])

# ------------------------------------------
# 2️⃣ READ ALL RECORDS
# ------------------------------------------
all_records = rpc.read_all(db, uid, password)
print("\nAll Records:")
for rec in all_records:
    print(rec)

# ------------------------------------------
# 3️⃣ UPDATE THE NEW RECORD
# ------------------------------------------
rpc.update(db, uid, password, new_id, {
    "remarks": "Updated via XML-RPC"
})
print("\nRecord Updated.")

# ------------------------------------------
# 4️⃣ DELETE THE RECORD (OPTIONAL)
# ------------------------------------------
# rpc.delete(db, uid, password, new_id)
# print("Record Deleted.")
