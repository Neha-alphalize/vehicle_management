import xmlrpc.client

class VehicleTrackingXMLRPC:

    def __init__(self, url):
        self.url = url.rstrip("/")
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        self.model = "vehicle.tracking"

    # --------------------------------------------------------
    # CREATE
    # --------------------------------------------------------
    def create(self, db, uid, password, values):
        return self.models.execute_kw(
            db, uid, password,
            self.model, "create",
            [values]
        )

    # --------------------------------------------------------
    # READ ONE
    # --------------------------------------------------------
    def read_one(self, db, uid, password, record_id, fields=None):
        if fields is None:
            fields = ["ref", "vehicle_id", "driver_id", "start_km", "end_km", "state"]
        result = self.models.execute_kw(
            db, uid, password,
            self.model, "read",
            [[record_id]],
            {"fields": fields}
        )
        return result[0]

    # --------------------------------------------------------
    # READ ALL
    # --------------------------------------------------------
    def read_all(self, db, uid, password, domain=None, fields=None):
        if domain is None:
            domain = []
        if fields is None:
            fields = ["ref", "vehicle_id", "driver_id", "start_km", "end_km", "state"]

        return self.models.execute_kw(
            db, uid, password,
            self.model, "search_read",
            [domain],
            {"fields": fields}
        )

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------
    def update(self, db, uid, password, record_id, values):
        return self.models.execute_kw(
            db, uid, password,
            self.model, "write",
            [[record_id], values]
        )

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------
    def delete(self, db, uid, password, record_id):
        return self.models.execute_kw(
            db, uid, password,
            self.model, "unlink",
            [[record_id]]
        )
