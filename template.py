import os

# Define folder structure
project_name = "video-notes-ai"

structure = {
    project_name: [
        "app/__init__.py",
        "app/main.py",
        "app/ui/__init__.py",
        "app/processing/__init__.py",
        "app/models/__init__.py",
        "app/utils/__init__.py",
        "data/",
        "tests/__init__.py",
        "docker/Dockerfile",
        ".github/workflows/ci.yml",
        "requirements.txt",
        "README.md",
        ".gitignore"
    ]
}

def create_structure():
    for base, paths in structure.items():
        for path in paths:
            full_path = os.path.join(base, path)
            dir_path = os.path.dirname(full_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            # Create empty files if not a directory
            if not path.endswith("/"):
                with open(full_path, "w") as f:
                    pass

if __name__ == "__main__":
    create_structure()
    print(f"✅ Project structure for '{project_name}' created successfully.")
