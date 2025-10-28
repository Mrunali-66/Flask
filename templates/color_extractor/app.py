from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
from sklearn.cluster import KMeans
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def rgb_to_hex(color):
    """Convert RGB tuple to HEX"""
    return '#{:02x}{:02x}{:02x}'.format(int(color[0]), int(color[1]), int(color[2]))


def extract_colors(image_path, num_colors=10):
    """Extract top N dominant colors using K-Means clustering"""
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Unable to read image")
        
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Reshape image to be a list of pixels
        image = image.reshape((-1, 3))
        
        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=num_colors, n_init=10, random_state=42)
        kmeans.fit(image)
        
        # Get the colors and their counts
        colors = kmeans.cluster_centers_.astype(int)
        labels = kmeans.labels_
        
        # Count occurrences of each cluster
        label_counts = np.bincount(labels)
        
        # Sort colors by frequency (most common first)
        sorted_indices = np.argsort(label_counts)[::-1]
        sorted_colors = colors[sorted_indices]
        
        # Convert to hex
        hex_colors = [rgb_to_hex(color) for color in sorted_colors]
        
        return hex_colors
    
    except Exception as e:
        print(f"Error extracting colors: {e}")
        return []


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main route for file upload"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'image' not in request.files:
            return redirect(request.url)
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return redirect(request.url)
        
        # Check if file is allowed
        if file and allowed_file(file.filename):
            # Secure the filename
            filename = secure_filename(file.filename)
            
            # Create unique filename to avoid conflicts
            import time
            unique_filename = f"{int(time.time())}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save file
            file.save(filepath)
            
            # Extract colors
            colors = extract_colors(filepath, num_colors=10)
            
            if colors:
                return render_template('result.html', colors=colors, image_file=unique_filename)
            else:
                # If color extraction fails, redirect back
                return redirect(url_for('index'))
        
        return redirect(url_for('index'))
    
    return render_template('index.html')


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return "File is too large. Maximum size is 16MB.", 413


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return "Page not found", 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return "Internal server error", 500


if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)