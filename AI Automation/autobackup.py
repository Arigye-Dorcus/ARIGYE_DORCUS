import os
import shutil
from datetime import datetime, timedelta

# Using your exact screenshot folder path
source_folder = r'C:\Users\user\Pictures\Screenshots'
backup_folder = r'C:\Users\user\Pictures\Screenshots_Backup'

def backup_recent_screenshots():
    try:
        # Verify source folder exists
        if not os.path.exists(source_folder):
            raise FileNotFoundError(f"Source folder not found: {source_folder}")

        # Create backup folder if needed (with exist_ok to prevent errors)
        os.makedirs(backup_folder, exist_ok=True)
        
        current_time = datetime.now()
        backed_up_files = 0
        
        print(f"Checking for new screenshots in: {source_folder}")
        
        for filename in os.listdir(source_folder):
            source_path = os.path.join(source_folder, filename)
            
            # Skip directories and system files
            if not os.path.isfile(source_path) or filename.startswith('.'):
                continue
                
            try:
                # Get modification time
                mod_time = datetime.fromtimestamp(os.path.getmtime(source_path))
                
                # Check if modified within last 3 minutes
                if current_time - mod_time <= timedelta(minutes=3):
                    # Create destination path
                    dest_path = os.path.join(backup_folder, filename)
                    
                    # Handle duplicate filenames
                    counter = 1
                    while os.path.exists(dest_path):
                        name, ext = os.path.splitext(filename)
                        dest_path = os.path.join(backup_folder, f"{name}_{counter}{ext}")
                        counter += 1
                    
                    # Copy file with all metadata
                    shutil.copy2(source_path, dest_path)
                    print(f"Backed up: {filename}")
                    backed_up_files += 1
                    
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
        
        if backed_up_files == 0:
            print("No new screenshots found (modified in last 3 minutes)")
        else:
            print(f"Backup complete. {backed_up_files} files copied to: {backup_folder}")
            
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        print("Possible solutions:")
        print("1. Make sure the folder exists")
        print("2. Run the script as Administrator")
        print("3. Check your OneDrive sync status if using cloud storage")

if __name__ == "__main__":
    backup_recent_screenshots()