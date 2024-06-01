def check_for_null_bytes(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        if b'\x00' in content:
            print(f"Null byte found in {file_path}")
            # print the line number
            lines = content.split(b'\n')
            for i, line in enumerate(lines):
                if b'\x00' in line:
                    print(f"Line {i}: {line}")

def check_and_clean_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    if b'\x00' in content:
        print(f"Null byte found in {file_path}. Attempting to clean...")
        clean_content = content.replace(b'\x00', b'')
        with open(file_path, 'wb') as file:
            file.write(clean_content)
        print(f"Cleaned {file_path}")

# List of your source filesd
source_files = [
    "Game/square.py",
    "Game/board.py",
    "main.py",
    "config.py",
]

for file in source_files:
    check_for_null_bytes(file)