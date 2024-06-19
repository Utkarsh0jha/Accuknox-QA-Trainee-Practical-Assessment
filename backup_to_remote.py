import os
import paramiko
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(filename='backup.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define backup parameters
SOURCE_DIR = '/path/to/source/directory'
REMOTE_SERVER = 'remote.server.com'
REMOTE_PORT = 22
REMOTE_USER = 'username'
REMOTE_PASSWORD = 'password'
REMOTE_DIR = '/path/to/remote/directory'

def create_backup_archive(source_dir):
    backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
    os.system(f"tar -czf {backup_filename} -C {source_dir} .")
    return backup_filename

def transfer_backup(backup_filename, remote_server, remote_port, remote_user, remote_password, remote_dir):
    try:
        transport = paramiko.Transport((remote_server, remote_port))
        transport.connect(username=remote_user, password=remote_password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(backup_filename, os.path.join(remote_dir, backup_filename))
        sftp.close()
        transport.close()

        logging.info(f'Successfully transferred {backup_filename} to {remote_server}:{remote_dir}')
        return True
    except Exception as e:
        logging.error(f'Failed to transfer {backup_filename} to {remote_server}:{remote_dir} - {str(e)}')
        return False

def main():
    logging.info('Starting backup process')

    # Create backup archive
    backup_filename = create_backup_archive(SOURCE_DIR)
    logging.info(f'Created backup archive: {backup_filename}')

    # Transfer backup to remote server
    success = transfer_backup(backup_filename, REMOTE_SERVER, REMOTE_PORT, REMOTE_USER, REMOTE_PASSWORD, REMOTE_DIR)

    if success:
        logging.info('Backup process completed successfully')
    else:
        logging.error('Backup process failed')

if __name__ == "__main__":
    main()
