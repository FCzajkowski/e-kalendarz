from flask import Flask, render_template, request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for local development

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
        return jsonify({"message": "Event added successfully!"}), 201

    # For GET request, return all events
    events = load_events()
    return jsonify(events)  # Return events as JSON

# Route for deleting an event by title
@app.route("/delete-event/<string:title>", methods=["DELETE"])
def delete_event(title):
    events = load_events()
    updated_events = [event for event in events if event["title"] != title]
    save_events(updated_events)
    return jsonify({"message": "Event deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
