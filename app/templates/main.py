from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify

main = Blueprint('main', __name__)

appliance_states = {
    'living-room': {'light': False, 'fan': False, 'ac': False},
    'kitchen-room': {'light': False, 'fan': False, 'ac': False},
    'washroom-room': {'light': False, 'fan': False, 'ac': False}
}

# Room routes for each room
@main.route("/home")
def home():
    if not session.get('logged_in'):  # If not logged in, redirect to login page
        return redirect(url_for('main.login'))
    return render_template("home.html")

@main.route("/api/toggle/<room_name>/<appliance>", methods=["POST"])
def toggle_appliance(room_name, appliance):
    if room_name in appliance_states:
        if appliance in appliance_states[room_name]:
            appliance_states[room_name][appliance] = not appliance_states[room_name][appliance]
            return jsonify({appliance: appliance_states[room_name][appliance]})
        return jsonify({"error": "Invalid appliance"}), 400
    return jsonify({"error": "Invalid room"}), 404

@main.route("/api/status/<room_name>")
def status(room_name):
    if room_name in appliance_states:
        return jsonify(appliance_states[room_name])
    return jsonify({"error": "Invalid room"}), 404

# Room page route (Example for Kitchen)
@main.route("/room/<room_name>")
def room(room_name):
    if not session.get('logged_in'):  # If not logged in, redirect to login page
        return redirect(url_for('main.login'))

    if room_name not in ['kitchen', 'washroom', 'livingroom']:
        return "Invalid room", 404

    return render_template("room.html", room_name=room_name)

