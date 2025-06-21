import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from metadata import generate_metadata, initialize_summarizer

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Checks if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Generate metadata
            metadata = generate_metadata(file_path)

            # Clean up the uploaded file
            os.remove(file_path)

            if metadata:
                return render_template('results.html', metadata=metadata)
            else:
                # Handle case where metadata generation fails
                return "Could not generate metadata for this file.", 400

    return render_template('index.html')

if __name__ == '__main__':
    # Initialize the model when the app starts
    initialize_summarizer()
    app.run(debug=True, port=5001) 