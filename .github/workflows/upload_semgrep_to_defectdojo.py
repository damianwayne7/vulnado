import requests
import sys
import os

def uploadToDefectDojo(is_new_import, token, url, product_name, engagement_name, filename):
    try:
        with open(filename, 'rb') as file:
            multipart_form_data = {
                'file': (filename, file),
                'scan_type': (None, 'Semgrep JSON Report'),
                'product_name': (None, product_name),
                'engagement_name': (None, engagement_name),
            }
            endpoint = '/api/v2/import-scan/' if is_new_import else '/api/v2/reimport-scan/'
            response = requests.post(
                url + endpoint,
                files=multipart_form_data,
                headers={'Authorization': 'Token ' + token}
            )
            response.raise_for_status()  # Raise an error for HTTP error responses
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        token = os.getenv("DEFECT_DOJO_API_TOKEN")
        if not token:
            raise ValueError("DEFECT_DOJO_API_TOKEN environment variable not set")
        if len(sys.argv) != 9:
            print('Usage: python3 upload_semgrep_to_defectdojo.py --host DOJO_URL --product PRODUCT_NAME --engagement ENGAGEMENT_NAME --report REPORT_FILE')
            sys.exit(1)

        url = sys.argv[2]
        product_name = sys.argv[4]
        engagement_name = sys.argv[6]
        report = sys.argv[8]

        uploadToDefectDojo(False, token, url, product_name, engagement_name, report)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
