import os
import sys
import shutil
import re

def normalize(name):
    # Видаляємо символи, які не є буквами або цифрами
    normalized_name = re.sub(r'\W+', '', name)
    # Замінюємо пробіли на підкреслення
    normalized_name = normalized_name.replace(' ', '_')
    return normalized_name


KNOWN_EXTENSIONS = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'video': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR')
}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()

def get_extension(filename: str) -> str:
    return os.path.splitext(filename)[1][1:].upper()  # перетворюємо розширення файлу на назву папки jpg -> JPG

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = get_extension(file)
            normalized_file_name = normalize(file)
            
            if file_extension in KNOWN_EXTENSIONS['images']:
                destination = os.path.join(folder_path, 'images')
            elif file_extension in KNOWN_EXTENSIONS['video']:
                destination = os.path.join(folder_path, 'video')
            elif file_extension in KNOWN_EXTENSIONS['documents']:
                destination = os.path.join(folder_path, 'documents')
            elif file_extension in KNOWN_EXTENSIONS['audio']:
                destination = os.path.join(folder_path, 'audio')
            elif file_extension in KNOWN_EXTENSIONS['archives']:
                destination = os.path.join(folder_path, 'archives')
                archive_name = os.path.splitext(file)[0]
                archive_folder = os.path.join(destination, archive_name)
                shutil.unpack_archive(file_path, archive_folder)
                continue
            else:
                # Unknown extension, leave the file unchanged
                continue
            
            os.makedirs(destination, exist_ok=True)
            destination_file = os.path.join(destination, normalized_file_name + '.' + file_extension)
            shutil.move(file_path, destination_file)
            
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir in KNOWN_EXTENSIONS:
                # Ignore folders with known categories
                continue
            elif dir == 'archives':
                # Ignore the folder where archives are unpacked
                continue
            else:
                # Recursively process nested folders
                process_folder(dir_path)
                if not os.listdir(dir_path):
                    # If the folder is empty after processing, remove it
                    os.rmdir(dir_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python sort.py <folder_path>')
        sys.exit(1)

    folder_path = sys.argv[1]
    print(f'Start in folder {folder_path}')
    process_folder(folder_path)
    
    # Print the list of files in each category
    for category, extensions in KNOWN_EXTENSIONS.items():
        category_path = os.path.join(folder_path, category)
        files = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
        print(f'Files in {category}:')
        for file in files:
            print(file)
    
    # Print the known and unknown extensions
    known_extensions = set(extension for extensions in KNOWN_EXTENSIONS.values() for extension in extensions)
    unknown_extensions = set()
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_extension = get_extension(file)
            if file_extension not in known_extensions:
                unknown_extensions.add(file_extension)
    
    print('Known extensions:')
    print(known_extensions)
    
    print('Unknown extensions:')
    print(unknown_extensions)
