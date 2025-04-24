from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import os

# Set the path to the templates folder
template_folder = os.path.join(os.getcwd(), 'app', 'templates')

# Assuming your 'static' folder is in the root of your project
static_folder = os.path.join(os.getcwd(),'app',  'static')

# Create the Flask app and specify the template folder AND the static folder
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

# Create the Flask app and specify the template folder
#app = Flask(__name__, template_folder=template_folder)

# Set a secret key for session management and flash messages
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# Dummy users for login (replace this with actual database logic if needed)
users = {
    'user1': 'password123',
    'user2': 'password456'
}

# Dummy data to store appliance states (for demonstration purposes)
rooms = {
    'living-room': {'light': False, 'fan': False, 'ac': False},
    'kitchen-room': {'light': False, 'fan': False, 'ac': False},
    'washroom-room': {'light': False, 'fan': False, 'ac': False},
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))  # Redirect to home page if logged in
    return render_template('login.html')  # Render login page if not logged in

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the username exists and the password matches
    if username in users and users[username] == password:
        session['username'] = username  # Store username in session
        return redirect(url_for('home'))  # Redirect to home page upon successful login
    else:
        flash('Invalid credentials. Please try again.')  # Flash an error message
        return redirect(url_for('index'))  # Redirect back to login page

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))  # Redirect to login if not logged in
    return render_template('home.html')  # Render home page for logged-in users

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    return redirect(url_for('index'))  # Redirect to login page after logout

@app.route('/api/toggle/<room>/<appliance>', methods=['POST'])
def toggle_appliance(room, appliance):
    # Ensure the user is logged in before toggling appliances
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401  # Return unauthorized if not logged in

    # Toggle the state of the appliance in the specified room
    if room in rooms and appliance in rooms[room]:
        rooms[room][appliance] = not rooms[room][appliance]
        return jsonify({appliance: rooms[room][appliance]})
    return jsonify({'error': 'Invalid room or appliance'}), 400

if __name__ == '__main__':
    app.run(debug=True)

