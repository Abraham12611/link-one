from flask import Flask, request, jsonify, redirect
import dropbox
import os

# Initialize Flask app
app = Flask(__name__)

# Dropbox access token
DROPBOX_ACCESS_TOKEN = 'your_dropbox_access_token'  # Replace with your Dropbox API access token
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# In-memory database to store file links and view status
file_links_db = {}

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})

    try:
        # Upload file to Dropbox
        file_path = f'/{file.filename}'
        dbx.files_upload(file.read(), file_path)

        # Create a shareable link for the file
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(file_path)
        shareable_link = shared_link_metadata.url

        # Store link in in-memory database (simulate a DB)
        file_links_db[shareable_link] = {
            'file_path': file_path,
            'viewed': False
        }

        return jsonify({'success': True, 'link': shareable_link})

    except dropbox.exceptions.ApiError as err:
        return jsonify({'success': False, 'error': str(err)})

@app.route('/view/<path:link>', methods=['GET'])
def view_file(link):
    # Validate if the link exists in the database
    if link not in file_links_db:
        return jsonify({'success': False, 'error': 'Invalid or expired link'})

    file_info = file_links_db[link]

    # Check if the file has already been viewed
    if file_info['viewed']:
        return jsonify({'success': False, 'error': 'This link has already been accessed once.'})

    # Mark file as viewed
    file_info['viewed'] = True

    # Revoke the link after first access
    try:
        dbx.sharing_revoke_shared_link(link)
    except dropbox.exceptions.ApiError as err:
        return jsonify({'success': False, 'error': str(err)})

    return jsonify({'success': True, 'message': 'Link accessed and revoked'})

if __name__ == '__main__':
    app.run(debug=True)
