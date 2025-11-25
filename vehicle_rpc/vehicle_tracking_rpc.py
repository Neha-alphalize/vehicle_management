import requests

class VehicleTrackingRPC:

    def __init__(self, url, db, uid, password):
        self.url = url.rstrip("/") + "/jsonrpc"
        self.db = db
        self.uid = uid
        self.password = password
        self.model = "vehicle.tracking"

    def _call(self, args):
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": args
            },
            "id": 1
        }

        response = requests.post(self.url, json=payload).json()
        if "error" in response:
            raise Exception(response["error"])
        return response.get("result")

    # CREATE
    def create(self, values):
        return self._call([
            self.db,
            self.uid,
            self.password,
            self.model,
            "create",
            [values]
        ])

    # READ (search_read)
    def read(self, domain=[], fields=[]):
        return self._call([
            self.db,
            self.uid,
            self.password,
            self.model,
            "search_read",
            [domain],
            {"fields": fields}
        ])

    # UPDATE
    def update(self, record_id, values):
        return self._call([
            self.db,
            self.uid,
            self.password,
            self.model,
            "write",
            [[record_id], values]
        ])

    # DELETE
    def delete(self, record_id):
        return self._call([
            self.db,
            self.uid,
            self.password,
            self.model,
            "unlink",
            [[record_id]]
        ])
