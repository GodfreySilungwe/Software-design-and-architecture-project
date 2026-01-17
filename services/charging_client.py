import json
import urllib.request
import urllib.error

class ChargingServiceClient:
    BASE_URL = "http://localhost:5001"

    def _post(self, endpoint, payload):
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.BASE_URL}{endpoint}",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            print("[Charging Service Error]", e)

    def start_charging(self, regnum):
        self._post("/charge/start", {"regnum": regnum})

    def stop_charging(self, regnum):
        self._post("/charge/stop", {"regnum": regnum})

    def get_status(self, regnum):
        try:
            with urllib.request.urlopen(
                f"{self.BASE_URL}/charge/status/{regnum}"
            ) as response:
                return json.loads(response.read())
        except urllib.error.URLError:
            return None
