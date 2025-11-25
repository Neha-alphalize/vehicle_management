from vehicle_tracking_rpc import VehicleTrackingRPC

# -----------------------------
# CONFIGURE YOUR ODOO
# -----------------------------
url = "http://localhost:8069"   # or your server URL
db = "odoo192"
uid = 2                         # admin = 2
password = "123"

rpc = VehicleTrackingRPC(url, db, uid, password)

# -----------------------------
# 1️⃣ CREATE
# -----------------------------
new_id = rpc.create({
    ""
    "vehicle_id": 3,
    "driver_id": 11,
    "source": "branch",
    "destination": "customer_site",
    "start_km": 300,
    "end_km": 550,
    "remarks": "Created via API"
})

print("Created ID =", new_id)
new_record = rpc.read(
    domain=[("id", "=", new_id)],
    fields=["ref", "vehicle_id", "driver_id"]
)

print("Generated Ref =", new_record[0]["ref"])
# -----------------------------
# 2️⃣ READ
# -----------------------------
records = rpc.read(
    domain=[],
    fields=["vehicle_id", "driver_id", "start_km", "end_km", "state"]
)

print("Records:", records)

# -----------------------------
# 3️⃣ UPDATE
# -----------------------------
rpc.update(new_id, {
    "remarks": "Updated via API",
    "state": "validated"
})

print("Record updated.")

# -----------------------------
# 4️⃣ DELETE
# -----------------------------
# rpc.delete(new_id)
# print("Record deleted.")
