from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage (simulates service DB)
charging_sessions = {}

@app.route("/charge/start", methods=["POST"])
def start_charging():
    data = request.json
    regnum = data.get("regnum")

    charging_sessions[regnum] = {
        "status": "charging",
        "charge": 0
    }

    return jsonify({
        "message": f"Charging started for {regnum}"
    }), 200


@app.route("/charge/status/<regnum>", methods=["GET"])
def charging_status(regnum):
    session = charging_sessions.get(regnum)

    if not session:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify(session), 200


@app.route("/charge/stop", methods=["POST"])
def stop_charging():
    data = request.json
    regnum = data.get("regnum")

    if regnum in charging_sessions:
        charging_sessions[regnum]["status"] = "stopped"

    return jsonify({
        "message": f"Charging stopped for {regnum}"
    }), 200


if __name__ == "__main__":
    app.run(port=5001)
