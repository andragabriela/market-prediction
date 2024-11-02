import os

from flask import Flask, render_template, redirect, url_for, flash, request
from controller.ReviewController import ReviewController

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize the controller
controller = ReviewController()

@app.route('/')
def index():
    # Serve index.html when visiting the root URL
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        # Call the controller’s scrape_data method
        controller.scrape_data()
        flash("Data scraping completed successfully!", "success")
    except Exception as e:
        flash(f"Error in scraping data: {e}", "danger")
    return redirect(url_for('index'))

@app.route('/load_data', methods=['POST'])
def load_data():
    try:
        controller.load_tabular_data()
        flash("Tabular data loaded successfully!", "success")
    except Exception as e:
        flash(f"Error in loading tabular data: {e}", "danger")
    return redirect(url_for('index'))

@app.route('/external_api', methods=['POST'])
def external_api():
    try:
        controller.call_external_api()
        flash("API data fetched successfully!", "success")
    except Exception as e:
        flash(f"Error in calling external API: {e}", "danger")
    return redirect(url_for('index'))

@app.route('/visualize', methods=['POST'])
def visualize():
    try:
        controller.create_visualization()
        flash("Visualization created successfully!", "success")
    except Exception as e:
        flash(f"Error in creating visualization: {e}", "danger")
    return redirect(url_for('index'))

@app.route('/json_load', methods=['POST'])
def json_load():
    # Ensure a file was uploaded
    if 'json_file' not in request.files:
        flash("No file selected", "danger")
        return redirect(url_for('index'))

    file = request.files['json_file']

    if file.filename == '':
        flash("No file selected", "danger")
        return redirect(url_for('index'))

    # Process the uploaded file directly
    try:
        # Use the repository function to load, validate, and save the JSON data
        data = controller.load_json_data(file)
        flash("JSON data loaded, validated, and saved successfully!", "success")

    except Exception as e:
        flash(f"Error in loading JSON data: {e}", "danger")

    return redirect(url_for('index'))

@app.route('/cluster', methods=['POST'])
def cluster():
    try:
        controller.build_segmentation_model()
        flash("Segmentation created successfully!", "success")
    except Exception as e:
        flash(f"Error in creating segmentation: {e}", "danger")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
