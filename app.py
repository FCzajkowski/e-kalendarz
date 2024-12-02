from flask import Flask, render_template, request, jsonify, make_response
import json

app = Flask(__name__)

DATA_FILE = "dates.json"

# Helper function to load events
def load_events():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Helper function to save events
def save_events(events):
    with open(DATA_FILE, "w") as file:
        json.dump(events, file, indent=4)

# Function to add CORS headers to the response
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"  # Allow all domains, can restrict to specific domain if needed
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

# Route for rendering index.html
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Route for getting and adding events
@app.route("/events", methods=["GET", "POST"])
def events():
    if request.method == "POST":
        # Handle adding a new event
        new_event = request.json
        events = load_events()

        # Check if the title already exists
        if any(event["title"] == new_event["title"] for event in events):
            return jsonify({"error": "Event with this title already exists!"}), 400

        # Add the new event
        events.append(new_event)
        save_events(events)
        response = jsonify({"message": "Event added successfully!"})
        return add_cors_headers(response), 201

    # For GET request, return all events
    events = load_events()
    response = jsonify(events)  # Return events as JSON
    return add_cors_headers(response)

# Route for deleting an event by title
@app.route("/delete-event/<string:title>", methods=["DELETE"])
def delete_event(title):
    events = load_events()
    updated_events = [event for event in events if event["title"] != title]
    save_events(updated_events)
    response = jsonify({"message": "Event deleted successfully!"})
    return add_cors_headers(response)

if __name__ == "__main__":
    app.run(debug=True)
