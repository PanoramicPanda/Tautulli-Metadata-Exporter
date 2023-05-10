import requests
import json
import time
import os
import shutil
import argparse
import logging
from datetime import datetime

def tautulli_request(cmd, params=None):
    if params is None:
        params = {}
    params.update({'apikey': args.api_key, 'cmd': cmd})
    response = requests.get(args.tautulli_url + '/api/v2', params=params)
    return response.json()

def main(args):
    try:
        # Prepare the destination file path
        destination_path = os.path.join(args.destination_folder, args.new_filename)
        if not args.overwrite and os.path.exists(destination_path):
            iso_date = datetime.now().strftime('%Y%m%d')
            destination_path = os.path.join(args.destination_folder, f"{os.path.splitext(args.new_filename)[0]}_{iso_date}{os.path.splitext(args.new_filename)[1]}")

        # Configure logging
        log_filename = os.path.join(args.destination_folder, f'{os.path.splitext(args.new_filename)[0]}_log.txt')
        logging.basicConfig(filename=log_filename, 
                        filemode='w', 
                        level=logging.INFO, 
                        format='%(asctime)s %(message)s', 
                        datefmt='%Y-%m-%dT%H:%M:%S')

        # Export the library
        logging.info("Exporting library...")
        export_params = {
            'section_id': args.library_id,
            'file_format': args.file_format or 'json',
            'metadata_level': args.metadata_level or 0,
            'media_info_level': args.media_info_level or 0
        }
        if args.custom_metadata_tags:
            export_params['custom_fields'] = ','.join(args.custom_metadata_tags)

        export_response = tautulli_request('export_metadata', export_params)

        # Find the latest generated entry based on "timestamp" and complete=0
        logging.info("Finding the latest generated entry...")
        exports_table_response = tautulli_request('get_exports_table', {'section_id': args.library_id})
        latest_export = max((export for export in exports_table_response['response']['data']['data'] if export['complete'] == 0), key=lambda x: x['timestamp'])
        export_id = latest_export['export_id']
        
        # Wait for the export to complete
        logging.info("Waiting for export to complete...")
        export_complete = False
        while not export_complete:
            time.sleep(5)
            status_response = tautulli_request('get_exports_table', {'section_id': args.library_id})
            current_export = next((export for export in status_response['response']['data']['data'] if export['export_id'] == export_id), None)
            if current_export:
                export_complete = (current_export['complete'] == 1)
            else:
                raise ValueError(f"Unable to find the export job with export_id {export_id}")

        # Download the export
        logging.info("Downloading export...")
        export_file = requests.get(args.tautulli_url + f'/api/v2', params={'apikey': args.api_key, 'cmd': 'download_export', 'export_id': export_id})
        with open(destination_path, 'wb') as f:
            f.write(export_file.content)

        # Delete the export
        logging.info("Deleting the export from the table...")
        tautulli_request('delete_export', {'export_id': export_id})

        logging.info("Done!")
    except Exception:
        logging.error("Exception occurred", exc_info=True)
	
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export library from Tautulli with custom metadata tags.')
    parser.add_argument('--tautulli_url', required=True, help='URL for your Tautulli instance.')
    parser.add_argument('--api_key', required=True, help='API key for your Tautulli instance.')
    parser.add_argument('--library_id', required=True, help='Library ID to export.')
    parser.add_argument('--destination_folder', required=True, help='Path to the destination folder.')
    parser.add_argument('--custom_metadata_tags', nargs='+', help='Optional custom metadata tags to include in the export.')
    parser.add_argument('--new_filename', required=True, help='New filename for the exported file.')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite the file if it already exists. If not provided or false, appends the current date in ISO format (YYYYMMDD) to the filename.')
    parser.add_argument('--metadata_level', type=int, help='Optional metadata level. Default is 0 if not provided.')
    parser.add_argument('--media_info_level', type=int, help='Optional media info level. Default is 0 if not provided.')
    parser.add_argument('--file_format', choices=['csv', 'json', 'xml', 'm3u'], help='Optional file format for the export. Default is "json" if not provided.')

    args = parser.parse_args()
    main(args)