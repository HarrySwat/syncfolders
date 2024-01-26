# Import necessary libraries
import os
import shutil
import time
import argparse
from datetime import datetime

# Function to synchronize folders
def synchro(source_path, replica_path, log_file):
    print(f"Synchronizing folders ")

# Loop through the files in the source folder 
    for root, dirs, files in os.walk(source_path):
        for file in files:
            source_file_path = os.path.join(root, file)
            replica_file_path = os.path.join(replica_path, os.path.relpath(source_file_path, source_path))

           # If the replica file doesn't exist, copy it from the source
            if not os.path.exists(replica_file_path):
                shutil.copy2(source_file_path, replica_file_path)
                 # Log the file copying action
                log(log_file, f"File copied: {source_file_path} -> {replica_file_path}")
            else:
                # If the replica file exists, check if it's newer in the source
                source_last_modified = os.path.getmtime(source_file_path)
                replica_last_modified = os.path.getmtime(replica_file_path)
                 # If the source file is newer, update the replica
                if source_last_modified > replica_last_modified:
                    shutil.copy2(source_file_path, replica_file_path)
                    log(log_file, f"File updated: {source_file_path} -> {replica_file_path}")
     # Loop through the files in the replica folder
    for root, dirs, files in os.walk(replica_path):
        for file in files:
            replica_file_path = os.path.join(root, file)
            source_file_path = os.path.join(source_path, os.path.relpath(replica_file_path, replica_path))
            # If the source  file doesn't exist, remove the replica file
            if not os.path.exists(source_file_path):
                os.remove(replica_file_path)
                log(log_file, f"File removed: {replica_file_path}")

    print("Synchronization complete.")

# Function to log messages
def log(log_file, message):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"

    with open(log_file, 'a') as log:
        log.write(log_entry + '\n')
    
    print(log_entry)
# Main  for  parsing and execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder synchronization program.")
    parser.add_argument("source", help="Source path.")
    parser.add_argument("replica", help="Replica path.")
    parser.add_argument("interval", type=int, help=" interval .")
    parser.add_argument("log_file", help="log path")
    args = parser.parse_args()

    print("Folder synchronization started")

    try:
        # Run the synchronization in an infinite loop
        while True:
            synchro(args.source, args.replica, args.log_file)
            # interval
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nFolder synchronization stopped.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        print("Folder synchronization stopped.")


    






