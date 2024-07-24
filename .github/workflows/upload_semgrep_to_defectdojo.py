import requests
import sys
import os
import argparse

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
    print("Upload successful.")
    print(response.json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload Semgrep results to DefectDojo.')
    parser.add_argument('--host', required=True, help='DefectDojo host URL')
    parser.add_argument('--product', required=True, help='Product name in DefectDojo')
    parser.add_argument('--engagement', required=True, help='Engagement name in DefectDojo')
    parser.add_argument('--report', required=True, help='Path to the Semgrep report file')
    parser.add_argument('--is_new_import', action='store_true', help='Flag to indicate if this is a new import')

    args = parser.parse_args()

    token = os.getenv("DEFECT_DOJO_API_TOKEN")
    if not token:
        print("Please set the environment variable DEFECT_DOJO_API_TOKEN")
        sys.exit(1)

    uploadToDefectDojo(args.is_new_import, token, args.host, args.product, args.engagement, args.report)
