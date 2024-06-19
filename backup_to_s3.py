import os
import boto3
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(filename='backup.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define backup parameters
SOURCE_DIR = '/path/to/source/directory'
BUCKET_NAME = 'your-s3-bucket-name'
S3_FOLDER = 'backups'

def create_backup_archive(source_dir):
    backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
    os.system(f"tar -czf {backup_filename} -C {source_dir} .")
    return backup_filename

def upload_to_s3(backup_filename, bucket_name, s3_folder):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(backup_filename, bucket_name, f"{s3_folder}/{backup_filename}")
        logging.info(f'Successfully uploaded {backup_filename} to s3://{bucket_name}/{s3_folder}')
        return True
    except Exception as e:
        logging.error(f'Failed to upload {backup_filename} to s3://{bucket_name}/{s3_folder} - {str(e)}')
        return False

def main():
    logging.info('Starting backup process')

    # Create backup archive
    backup_filename = create_backup_archive(SOURCE_DIR)
    logging.info(f'Created backup archive: {backup_filename}')

    # Upload backup to S3
    success = upload_to_s3(backup_filename, BUCKET_NAME, S3_FOLDER)

    if success:
        logging.info('Backup process completed successfully')
    else:
        logging.error('Backup process failed')

if __name__ == "__main__":
    main()
