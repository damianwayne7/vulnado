import requests
import sys
import os

def uploadToDefectDojo(is_new_import, token, url, product_name, engagement_name, filename):
    multipart_form_data = {
        'file': (filename, open(filename, 'rb')),
        'scan_type': (None, 'Semgrep JSON Report'),
        'product_name': (None, product_name),
        'engagement_name': (None, engagement_name),
    }

    endpoint = '/api/v2/import-scan/' if is_new_import else '/api/v2/reimport-scan/'
    response = requests.post(
        url + endpoint,
        files=multipart_form_data,
        headers={
            'Authorization': 'Token ' + token,
        }
    )
    if response.status_code != 200:
        sys.exit(f'Post failed: {response.text}')
    print(response.text)

if __name__ == "__main__":
    if len(sys.argv) == 9:
        token = os.getenv("DEFECT_DOJO_API_TOKEN")
        if token is None:
            print("Please set the environment variable DEFECT_DOJO_API_TOKEN")
            sys.exit(1)
        url = sys.argv[2]
        product_name = sys.argv[4]
        engagement_name = sys.argv[6]
        report = sys.argv[8]
        uploadToDefectDojo(False, token, url, product_name, engagement_name, report)
    else:
        print('Usage: python3 upload_semgrep_to_defectdojo.py --host DOJO_URL --product PRODUCT_NAME --engagement ENGAGEMENT_NAME --report REPORT_FILE')
