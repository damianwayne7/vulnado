import json
from defectdojo_api import defectdojo

# Hardcoded DefectDojo connection details
DEFECTDOJO_URL = "http://13.213.67.252:8000"
DEFECTDOJO_API_KEY = "1b9c5ac045cfec60f3b508e969a6d3b7d3f52247"
DEFECTDOJO_ENGAGEMENT_ID = "linter_scan"
DEFECTDOJO_USER = "admin"

class CustomDefectDojoAPI(defectdojo.DefectDojoAPI):
    def __init__(self, host, api_key, user, verify_ssl):
        # Custom initialization to fix the issue with the host.split('/')
        self.api_key = api_key
        self.user = user
        self.verify_ssl = verify_ssl
        self.host = host.rstrip('/')
        self.api_v2_key = api_key  # Assuming api_key is for v2 API

# Initialize the DefectDojo connection using the custom class
dojo = CustomDefectDojoAPI(
    host=DEFECTDOJO_URL,
    api_key=DEFECTDOJO_API_KEY,
    user=DEFECTDOJO_USER,
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
