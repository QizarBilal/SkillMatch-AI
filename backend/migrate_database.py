import sqlite3
import os

db_path = "skillmatch.db"

if not os.path.exists(db_path):
    print(f"Database {db_path} not found. It will be created automatically when you run the server.")
    exit(0)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Checking existing columns in submissions table...")
cursor.execute("PRAGMA table_info(submissions)")
existing_columns = {row[1] for row in cursor.fetchall()}
print(f"Existing columns: {existing_columns}")

new_columns = {
    'resume_clean_text': 'TEXT',
    'resume_tokens': 'TEXT',
    'resume_skills': 'TEXT',
    'jd_clean_text': 'TEXT',
    'jd_tokens': 'TEXT',
    'jd_skills': 'TEXT'
}

columns_added = 0
for column_name, column_type in new_columns.items():
    if column_name not in existing_columns:
        try:
            cursor.execute(f"ALTER TABLE submissions ADD COLUMN {column_name} {column_type}")
            print(f"✓ Added column: {column_name}")
            columns_added += 1
        except sqlite3.OperationalError as e:
            print(f"✗ Error adding column {column_name}: {e}")
    else:
        print(f"  Column {column_name} already exists")

conn.commit()
conn.close()

if columns_added > 0:
    print(f"\n✓ Successfully added {columns_added} new column(s)")
else:
    print("\n✓ Database schema is up to date")

print("\nYou can now restart your server.")
