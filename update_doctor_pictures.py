import sqlite3
import os

# Path to your database
db_path = r"E:\programs\healthcare\instance\database.db"

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get current doctor pictures
cursor.execute("SELECT id, name, picture FROM doctor")
doctors = cursor.fetchall()

print("Current doctor pictures:")
for doc in doctors:
    print(f"ID: {doc[0]}, Name: {doc[1]}, Picture: {doc[2]}")

# Directory with profile photos
photo_dir = r"E:\programs\healthcare\static\profile_photo"

# Get list of .jpg files
jpg_files = [f for f in os.listdir(photo_dir) if f.endswith('.jpg')]
print(f"\nAvailable .jpg files: {jpg_files}")

# Update pictures to add .jpg if not present and file exists, and fix the path
for doc in doctors:
    doc_id, name, picture = doc
    if picture:
        # Remove 'static/' prefix if present
        if picture.startswith('static/'):
            picture = picture[7:]  # Remove 'static/'
        if not picture.endswith('.jpg'):
            # Extract the base name, e.g., 'profile_photo/doc1' -> 'doc1'
            base_name = os.path.basename(picture)
            jpg_file = base_name + '.jpg'
            if jpg_file in jpg_files:
                new_picture = picture + '.jpg'
                cursor.execute("UPDATE doctor SET picture = ? WHERE id = ?", (new_picture, doc_id))
                print(f"Updated {name}: {picture} -> {new_picture}")
            else:
                print(f"No .jpg file for {name}: {picture}")
        else:
            # Already has .jpg, but ensure path is correct
            cursor.execute("UPDATE doctor SET picture = ? WHERE id = ?", (picture, doc_id))
            print(f"Path corrected for {name}: {picture}")
    else:
        print(f"No picture for {name}")

conn.commit()
conn.close()

print("Database update completed.")
