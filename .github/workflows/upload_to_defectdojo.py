import json
from defectdojo_api import defectdojo

# Hardcoded DefectDojo connection details
DEFECTDOJO_URL = "http://13.213.67.252:8080"
DEFECTDOJO_API_KEY = "1b9c5ac045cfec60f3b508e969a6d3b7d3f52247"
DEFECTDOJO_ENGAGEMENT_ID = "linter_scan"

# Initialize the DefectDojo connection
dojo = defectdojo.DefectDojoAPI(
    host=DEFECTDOJO_URL,
    api_key=DEFECTDOJO_API_KEY,
    verify_ssl=False  # Change to True if using HTTPS and a valid SSL certificate
)

# Read the SARIF report
report_path = 'reports/super-linter.sarif'
try:
    with open(report_path, 'r') as report_file:
        report_content = json.load(report_file)

    # Upload the report
    response = dojo.upload_sarif(
        engagement_id=DEFECTDOJO_ENGAGEMENT_ID,
        file=report_content,
        scan_type='Sarif',
        active=True,
        verified=False
    )

    if response.success:
        print("Upload successful!")
    else:
        print(f"Upload failed: {response.message}")
except Exception as e:
    print(f"Error reading or uploading report: {str(e)}")
