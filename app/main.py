from flask import session, redirect, url_for, flash
from flask import Blueprint, render_template, jsonify, request
from flask_cors import CORS

main = Blueprint('main', __name__)

# Store appliance states in Blueprint scope (for now; can be moved to a database or Flask config)
appliances = {
    "light": False,
    "fan": False,
    "ac": False
}

@main.record
def init_app(setup_state):
    # Enable CORS when the blueprint is registered
    CORS(setup_state.app)

# ✅ Login Page
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "1234":  # Simple hardcoded credentials
            session["logged_in"] = True
            return redirect(url_for("main.home"))
        flash("Invalid credentials!")
    return render_template("login.html")

# ✅ Logout
@main.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("main.login"))

# ✅ Protected Home Page
@main.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("main.login"))
    return redirect(url_for("main.home"))  # Redirect to home after login
#✅ Home Page
@main.route("/home")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("main.login"))
    return render_template("home.html")

# ✅ Appliance status API
@main.route("/api/status")
def status():
    return jsonify(appliances)

# ✅ Toggle appliance
@main.route("/api/toggle/<appliance>", methods=["POST"])
def toggle_appliance(appliance):
    if appliance in appliances:
        appliances[appliance] = not appliances[appliance]
        return jsonify({appliance: appliances[appliance]})
    return jsonify({"error": "Invalid appliance"}), 400

