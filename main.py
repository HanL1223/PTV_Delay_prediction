import os

def create_project_structure(base_dir="ptv_train_project"):
    dirs = [
        "data/raw",
        "data/processed",
        "scripts",
        "notebooks",
        "models",
        "utils",
        "dashboard",
        "config"
    ]

    files = {
        "README.md": "# PTV Train Delay Prediction Project\n\nDocument your goals, setup, and usage here.",
        "requirements.txt": "# Add Python dependencies here\npandas\nrequests\nscikit-learn",
        "scripts/fetch_departures.py": "# Fetch data from PTV API",
        "scripts/train_model.py": "# Train ML model",
        "utils/ptv_api.py": "# Helper functions for signing and calling the PTV API",
        "dashboard/app.py": "# Streamlit or Flask app"
    }

    print(f"Creating project in: {base_dir}")
    os.makedirs(base_dir, exist_ok=True)

    for d in dirs:
        os.makedirs(os.path.join(base_dir, d), exist_ok=True)
        print(f"Created directory: {d}")

    for file, content in files.items():
        path = os.path.join(base_dir, file)
        with open(path, "w") as f:
            f.write(content)
        print(f"Created file: {file}")

    print("\n✅ Project structure created successfully.")

if __name__ == "__main__":
    create_project_structure()
