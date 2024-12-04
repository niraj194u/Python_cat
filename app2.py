from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
items = [
    {"id": 1, "name": "Item 1", "price": 100},
    {"id": 2, "name": "Item 2", "price": 200},
]

# Root route
@app.route('/', methods=['GET'])
def home():
    """
    Handle requests to the root URL.
    """
    return jsonify({"message": "Welcome to the Flask API! Available endpoints: /items"}), 200

# GET Method
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# POST Method
@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    new_item = {
        "id": len(items) + 1,
        "name": data.get("name"),
        "price": data.get("price")
    }
    items.append(new_item)
    return jsonify(new_item), 201

# PUT Method
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        item.update({
            "name": data.get("name", item["name"]),
            "price": data.get("price", item["price"])
        })
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

# DELETE Method
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": f"Item {item_id} deleted"}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
