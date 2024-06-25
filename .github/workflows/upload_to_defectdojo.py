import json
from defectdojo_api import defectdojo
import os

# Initialize the DefectDojo connection
dojo = defectdojo.DefectDojoAPI(
    host=os.environ["DEFECTDOJO_URL"],
    api_token=os.environ["DEFECTDOJO_API_KEY"],
    api_v2_key=os.environ["DEFECTDOJO_API_KEY"],
    user="",
    verify_ssl=True
)

# Read the SARIF report
report_path = 'reports/super-linter.sarif'
try:
    with open(report_path, 'r') as report_file:
        report_content = json.load(report_file)

    # Upload the report
    response = dojo.upload_sarif(
        engagement_id=os.environ["DEFECTDOJO_ENGAGEMENT_ID"],
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
