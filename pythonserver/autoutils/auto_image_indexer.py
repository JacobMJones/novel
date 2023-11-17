import os
import time
from datetime import datetime
from PIL import Image
from openpyxl import load_workbook, Workbook

def process_images():
    folder_path = '../images'  # Replace with your folder path
    file_names = os.listdir(folder_path)

    excel_file = '../image_data.xlsx'

    # Check if the Excel file already exists
    if os.path.exists(excel_file):
        wb = load_workbook(excel_file)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        # Added 'timestamp' and 'id' to the header row
        ws.append(['id', 'file', 'width', 'height', 'size', 'format', 'type', 'subtype', 'tags', 'votes', 'active', 'timestamp'])

    # Read existing file names from the Excel sheet to avoid duplicates
    seen_files = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        seen_files.add(row[1])  # Assuming file names are in the second column

    # Calculate next_id for new entries
    numeric_values = [row[0] for row in ws.iter_rows(min_row=2, max_col=1, values_only=True) if isinstance(row[0], (int, float))]

    if numeric_values:
        next_id = max(numeric_values) + 1
    else:
        next_id = 1  # Starting ID if no numeric values are present

    # Append data for new images with a timestamp
    for file_name in file_names:
        if file_name not in seen_files and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(folder_path, file_name)
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    file_size = os.path.getsize(file_path)
                    image_format = img.format
                    # Get the current timestamp
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # Append all data including the id and timestamp
                    ws.append([next_id, file_name, width, height, file_size, image_format, 'image', '', '', 0, 1, timestamp])
                    next_id += 1
                    seen_files.add(file_name)
                    print(f'Indexed file: {file_name}')
            except IOError:
                print(f'Cannot open file: {file_name}')

    # Save the workbook
    wb.save(excel_file)
    print("Processing complete.")

# Run the process in an infinite loop
while True:
    process_images()
    print("Waiting for next run...")
    time.sleep(120)  # Wait for 120 seconds (2 minutes)
