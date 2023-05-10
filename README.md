# Tautulli Metadata Exporter

## Description

This Python script uses Tautulli's API to export metadata from a specified library to a file, waits for the export to complete, and then deletes the export from Tautulli.

## Requirements

- Python 3.x
- Requests library (install via `pip install requests`)

## Usage

1. Ensure you have Python 3.x installed on your system.
2. Install the Requests library if you haven't already (pip install requests).
3. Save the Tautulli export script as a .py file, e.g., tautulli_export.py.
4. Run the script from the command line or terminal with the required arguments:

## Required Arguments

- `tautulli_url`: The URL of your Tautulli instance, e.g., `http://localhost:8181`.
- `api_key`: Your Tautulli API key.
- `library_id`: The ID of the library you want to export, e.g. `1`.
- `destination_folder`: The path to the folder where you want to store the exported file.
- `new_filename`: The new name of the exported file, e.g., `exported_library.json`.

## Optional Arguments

- `overwrite`: If set, the script will overwrite an existing file with the same name. If not set, the script will append the current date to the filename to avoid overwriting.
- `file_format`: The format of the export file. Can be 'csv', 'json', 'xml', or 'm3u'. Defaults to 'json'.
- `metadata_level`: The level of metadata to export. If not provided, defaults to 0.
- `media_info_level`: The level of media info to export. If not provided, defaults to 0.
- `custom_fields`: Space separated list of custom fields to export in addition to the export level selected. If not provided, it will not be included in the export parameters.

Example usage:

```bash
python3 tautulli_md_exporter.py --tautulli_url=http://localhost:8181 --api_key=YOUR_API_KEY --library_id=1 --destination_folder=/path/to/destination/ --new_filename=new_export.json --overwrite --file_format=json --custom_fields=title year collections.tag
```

## Setting up as a cron job

To run this script regularly, you can set up a cron job on your Linux system. Follow these steps:

1. Open the crontab editor by running `crontab -e`.
2. Add a new line with the following format: `* * * * * /usr/bin/python3 /path/to/tautulli_md_exporter.py --tautulli_url=http://localhost:8181 --api_key=YOUR_API_KEY --library_id=1 --destination_folder=/path/to/destination/ --new_filename=new_export.json --overwrite --file_format=json --custom_fields=title year collections.tag > /dev/null 2>&1`
   - Replace `/usr/bin/python3` with the path to your Python executable if it's located elsewhere.
   - Replace `/path/to/tautulli_md_exporter.py` with the path to this script.
   - Replace the other options as necessary.
   - The `> /dev/null 2>&1` part at the end will discard the standard output and standard error. If you want to keep a log, you can replace `/dev/null` with the path to a log file.
3. Save and exit the editor. The cron job will now run at the interval specified by the asterisks at the beginning of the line. For example, to run the script every day at 3 AM, you would use `0 3 * * *`.

Remember to give the script execute permissions (`chmod +x /path/to/tautulli_md_exporter.py`) and ensure that the user running the cron job has the necessary permissions for the script and the destination folder.
