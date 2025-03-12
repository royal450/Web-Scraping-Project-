from flask import Flask, render_template, request, flash, send_file
import os
import logging
from scraper import WebScraper
import pandas as pd
import tempfile
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Create temp directory if it doesn't exist
TEMP_DIR = Path(tempfile.gettempdir()) / 'web_scraper'
TEMP_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    elements = request.form.get('elements')

    if not url:
        flash('Please enter a URL', 'error')
        return render_template('index.html')

    try:
        scraper = WebScraper()
        data = scraper.scrape(url, elements)

        # Create temporary CSV file with a unique name
        file_name = f'scraped_data_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.csv'
        temp_file = TEMP_DIR / file_name
        pd.DataFrame(data).to_csv(temp_file, index=False)

        return render_template('result.html', data=data, file_name=file_name)

    except Exception as e:
        logger.error(f"Scraping error: {str(e)}")
        flash(f'Error during scraping: {str(e)}', 'error')
        return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    try:
        file_path = TEMP_DIR / filename
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {filename}")

        return send_file(
            file_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name='scraped_data.csv'
        )
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        flash(f'Error downloading file: {str(e)}', 'error')
        return render_template('index.html')

# Cleanup old files
def cleanup_old_files():
    try:
        current_time = pd.Timestamp.now()
        for file in TEMP_DIR.glob('*.csv'):
            # Remove files older than 1 hour
            if current_time - pd.Timestamp(file.stat().st_mtime, unit='s') > pd.Timedelta(hours=1):
                file.unlink()
    except Exception as e:
        logger.error(f"Error cleaning up files: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)