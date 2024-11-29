from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
items = [
    {"id": 1, "name": "Item 1", "price": 100},
    {"id": 2, "name": "Item 2", "price": 200},
]

# Route to get all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# Route to get a single item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

# Route to add a new item
@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    new_item = {
        "id": len(items) + 1,
        "name": data["name"],
        "price": data["price"]
    }
    items.append(new_item)
    return jsonify(new_item), 201

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
