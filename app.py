from flask import Flask, request, jsonify, render_template
from model.media_layout_generator import MediaLayoutGenerator

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET'])
def home():
    return render_template('test_page.html')

@app.route('/generate-layout', methods=['POST'])
def generate_layout():
    try:
        data = request.json
        media_objects = data.get('media_objects', [])
        screen_width = data.get('screen_width', 1920)
        screen_height = data.get('screen_height', 1080)
        target_screen_width = data.get('target_screen_width', 1920)
        target_screen_height = data.get('target_screen_height', 1080)

        generator = MediaLayoutGenerator(screen_width, screen_height)
        layout = generator.generate_layout(media_objects, target_screen_width, target_screen_height)

        # Add default x and y coordinates if missing
        for layer, items in layout.items():
            for item in items:
                item.setdefault("x", 0)
                item.setdefault("y", 0)

        # Validate the generated layout
        def validate_layout(layout):
            for layer_name, items in layout.items():
                total_area = sum(item["width"] * item["height"] for item in items)
                for item in items:
                    if item["width"] * item["height"] > total_area / 2:
                        print(f"Warning: Large media object {item} should be in a separate layer.")

        validate_layout(layout)

        return jsonify({"layout": layout}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/player', methods=['GET'])
def player():
    return render_template('player.html')

if __name__ == '__main__':
    app.run(debug=True)
