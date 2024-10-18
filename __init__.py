from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configurations from config.py
    app.config.from_object('config')

    # Import routes
    from .routes import upload_file, view_file

    # Register routes
    app.add_url_rule('/upload', 'upload_file', upload_file, methods=['POST'])
    app.add_url_rule('/view/<path:link>', 'view_file', view_file, methods=['GET'])

    return app
