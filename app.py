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
        target_screen_width = data.get('screen_width', 1920)
        target_screen_height = data.get('screen_height', 1080)

        generator = MediaLayoutGenerator(screen_width, screen_height)
        layout = generator.generate_layout(media_objects, target_screen_width, target_screen_height)

        return jsonify({"layout": layout}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/player', methods=['GET'])
def player():
    return render_template('player.html')

if __name__ == '__main__':
    app.run(debug=True)
