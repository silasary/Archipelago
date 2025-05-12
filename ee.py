import tempfile
import zipfile
import os

with tempfile.TemporaryDirectory() as tmpdir:
    zip_path = os.path.join(tmpdir, "test.zip")

    # Create a test ZIP file
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr("example.txt", "Hello, world!")

    print(f"ZIP file created at: {zip_path}")
    input("Press Enter to exit (this will delete the temp directory)...")