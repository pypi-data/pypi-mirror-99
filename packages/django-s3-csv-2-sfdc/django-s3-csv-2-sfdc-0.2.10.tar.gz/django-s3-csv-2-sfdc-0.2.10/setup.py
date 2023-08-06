# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_s3_csv_2_sfdc']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.6,<4.0.0',
 'boto3>=1.17.3,<2.0.0',
 'simple-salesforce>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'django-s3-csv-2-sfdc',
    'version': '0.2.10',
    'description': 'A set of helper functions for CSV to Salesforce procedures, with reporting in AWS S3, based in a Django project',
    'long_description': "# Overview\n\nA set of helper functions for CSV to Salesforce procedures, with reporting in AWS S3, based in a Django project.\nThe use case is extremely specific, but the helpers should be modular so they can be cherry-picked.\n\nTypical use case:\n\n- Receive an S3 event\n- Download the S3 object\n- Serialize the file into JSON\n- Bulk upsert the JSON data to Salesforce\n- Parse the results of the upsert for errors\n- Construct a CSV error report\n- Move the triggering S3 object to an archive folder\n- Push the error report to an error folder in the same bucket\n- Push an object to Salesforce that details information about the above execution\n\n# Example\n\n```python\nfrom django_s3_csv_2_sfdc.csv_helpers import create_error_report\nfrom django_s3_csv_2_sfdc.s3_helpers import download_file, respond_to_s3_event, upload_file\nfrom django_s3_csv_2_sfdc.sfdc_helpers import extract_errors_from_results\n\n\n# handler for listening to s3 events\ndef handler(event, context):\n    respond_to_s3_event(event, download_and_process)\n\n\ndef download_and_process(s3_object_key, bucket_name):\n    download_path = download_file(s3_object_key, bucket_name)\n\n    # This function contains your own biz logic; does not come from this library\n    results = serialize_and_push_to_sfdc(download_path)\n\n    sucesses, errors = parse_bulk_upsert_results(results)\n\n    report_path, errors_count = create_error_report([errors])\n\n    upload_file(report_path, bucket_name)\n```\n\nJust take what'cha need!\n",
    'author': 'Alex Drozd',
    'author_email': 'drozdster@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brno32/django-s3-csv-2-sfdc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
