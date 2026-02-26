import os

print("=" * 60)
print("DIAGNOSTIC: Checking Project Structure")
print("=" * 60)

# Current directory
print(f"\n✓ Current Directory: {os.getcwd()}")

# List all files and folders
print("\n✓ Files/Folders in Current Directory:")
for item in os.listdir('.'):
    print(f"  - {item}")

# Check functions folder
print("\n✓ Contents of 'functions' folder:")
if os.path.exists('functions'):
    for item in os.listdir('functions'):
        print(f"  - {item}")
else:
    print("  ❌ 'functions' folder does NOT exist!")

# Check __init__.py
print("\n✓ Checking __init__.py:")
if os.path.exists('functions/__init__.py'):
    print("  ✓ functions/__init__.py EXISTS")
else:
    print("  ❌ functions/__init__.py does NOT exist!")

# Check function files
print("\n✓ Checking function files:")
expected_files = [
    'func_remove_duplicates.py',
    'func_trim_whitespace.py',
    'func_fill_missing_values.py',
    'func_standardize_date_formats.py',
    'func_sanitize_special_characters.py'
]

for file in expected_files:
    path = f'functions/{file}'
    if os.path.exists(path):
        print(f"  ✓ {file}")
    else:
        print(f"  ❌ {file} MISSING!")

print("\n" + "=" * 60)