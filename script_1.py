# Create requirements.txt file for dependencies
requirements_content = '''streamlit>=1.28.0
moondream>=0.1.0
Pillow>=9.0.0
numpy>=1.21.0
pandas>=1.3.0
'''

with open("requirements.txt", "w") as f:
    f.write(requirements_content)

# Create a .streamlit/config.toml for better UI
config_content = '''[theme]
primaryColor = "#ff6b6b"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
maxUploadSize = 200
'''

import os
os.makedirs(".streamlit", exist_ok=True)
with open(".streamlit/config.toml", "w") as f:
    f.write(config_content)

# Create a sample secrets.toml file (user will need to add their actual API key)
secrets_sample_content = '''# Copy this file to .streamlit/secrets.toml and add your actual API key
# MOONDREAM_API_KEY = "your_actual_api_key_here"

# Instructions:
# 1. Get your API key from https://console.moondream.ai
# 2. Uncomment the line above and replace with your actual key
# 3. Make sure to add .streamlit/secrets.toml to your .gitignore file
'''

with open(".streamlit/secrets_sample.toml", "w") as f:
    f.write(secrets_sample_content)

# Create .gitignore file
gitignore_content = '''.streamlit/secrets.toml
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.env
'''

with open(".gitignore", "w") as f:
    f.write(gitignore_content)

print("✅ Supporting files created!")
print("\nAdditional files created:")
print("- requirements.txt (Python dependencies)")
print("- .streamlit/config.toml (Streamlit configuration)")
print("- .streamlit/secrets_sample.toml (API key template)")
print("- .gitignore (Git ignore rules)")