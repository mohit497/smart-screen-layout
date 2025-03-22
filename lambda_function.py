import json
from model.media_layout_generator import MediaLayoutGenerator

def lambda_handler(event, context):
    try:
        media_objects = event['media_objects']
        generator = MediaLayoutGenerator(screen_width=1920, screen_height=1080)
        layout = generator.generate_layout(media_objects)
        return {
            'statusCode': 200,
            'body': json.dumps(layout)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }