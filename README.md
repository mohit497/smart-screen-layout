# smart-screen

Data model for creating adaptive layouts for screens based on size.

## API

### Endpoint: `/generate-layout`
- **Method**: POST
- **Request Body**:
  ```json
  {
      "media_objects": [
          { "type": "video", "width": 1280, "height": 720, "duration": 30 },
          { "type": "picture", "width": 600, "height": 400 },
          { "type": "text", "width": 800, "height": 200, "text": "Hello World" }
      ],
      "screen_width": 1920,
      "screen_height": 1080
  }
  ```
- **Response**:
  ```json
  {
      "layout": [
          { "type": "video", "x": 0, "y": 0, "width": 1280, "height": 720 },
          { "type": "picture", "x": 1300, "y": 100, "width": 600, "height": 400 },
          { "type": "text", "x": 100, "y": 800, "width": 800, "height": 200, "text": "Hello World" }
      ]
  }
  ```

## How to Start the API

1. Install the required dependencies:
   ```bash
   pip install flask
   ```

2. Run the Flask server:
   ```bash
   python app.py
   ```

3. The API will be available at `http://127.0.0.1:5000`.

## HTML Player

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open `http://127.0.0.1:5000/templates/player.html` in your browser to view the media layout.
