import requests
import sys

def upload_to_defectdojo(is_new_import, token, url, product_name, engagement_name, filename):
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

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Upload Semgrep results to DefectDojo')
    parser.add_argument('--host', required=True, help='DefectDojo URL')
    parser.add_argument('--token', required=True, help='DefectDojo API token')
    parser.add_argument('--product', required=True, help='DefectDojo product name')
    parser.add_argument('--engagement', required=True, help='DefectDojo engagement name')
    parser.add_argument('--report', required=True, help='Path to the Semgrep JSON report')
    parser.add_argument('--is_new_import', action='store_true', help='Indicate if this is a new import')
    
    args = parser.parse_args()

    upload_to_defectdojo(args.is_new_import, args.token, args.host, args.product, args.engagement, args.report)
