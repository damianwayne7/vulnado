import json
from defectdojo_api import defectdojo

# Hardcoded DefectDojo connection details
DEFECTDOJO_URL = "http://13.213.67.252:8000"
DEFECTDOJO_API_KEY = "1b9c5ac045cfec60f3b508e969a6d3b7d3f52247"
DEFECTDOJO_ENGAGEMENT_ID = "linter_scan"
DEFECTDOJO_USER = "admin"

# Initialize the DefectDojo connection
dojo = defectdojo.DefectDojoAPI(
    host=DEFECTDOJO_URL,
    api_key=DEFECTDOJO_API_KEY,
    user="",
    verify_ssl=False
)

# Read the SARIF report
report_path = 'reports/super-linter.sarif'
try:
    with open(report_path, 'r') as report_file:
        report_content = json.load(report_file)

    # Write the content to a file
    with open('/tmp/super-linter.sarif', 'w') as tmp_report_file:
        json.dump(report_content, tmp_report_file)

    # Upload the report
    response = dojo.upload_sarif_scan(
        engagement_id=DEFECTDOJO_ENGAGEMENT_ID,
        file='/tmp/super-linter.sarif',
        scan_type='Sarif',
        active=True,
        verified=False
    )

    if response.success:
        print("Upload successful!")
    else:
        print(f"Upload failed: {response.message}")
except FileNotFoundError:
    print(f"Error: Report file not found: {report_path}")
except Exception as e:
    print(f"Error reading or uploading report: {str(e)}")
