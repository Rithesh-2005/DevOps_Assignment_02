from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import uuid # To generate unique IDs for tickets

app = Flask(__name__)

# Route for the homepage, which will display the booking form
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route to handle ticket booking form submission
@app.route('/book', methods=['POST'])
def book_ticket():
    # Get data from the form
    your_name = request.form.get('your_name')
    event_name = request.form.get('event_name')

    # Basic validation (optional, but good practice)
    if not your_name or not event_name:
        return jsonify({"error": "Both 'Your name' and 'Event name' are required"}), 400

    # Generate a simple ticket object (in a real app, this would save to a database)
    ticket_id = str(uuid.uuid4()) # Unique ID
    created_at = datetime.now().isoformat() + "Z" # ISO format with 'Z' for UTC

    ticket_data = {
        "id": ticket_id,
        "name": your_name,
        "event": event_name,
        "createdAt": created_at
    }

    # For this demo, we just return the ticket data as JSON
    # In a real application, you might redirect to a confirmation page
    # or display the ticket data in the rendered HTML.
    return jsonify(ticket_data), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)