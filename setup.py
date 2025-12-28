"""
Setup script for Django System Call Optimizer
Run this script to set up the project for the first time
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a shell command"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    print("=" * 50)
    print("Django System Call Optimizer - Setup")
    print("=" * 50)
    
    # Check if Django is installed
    print("\n1. Checking Django installation...")
    if not run_command("python -m django --version"):
        print("Django not found. Installing dependencies...")
        if not run_command("pip install -r requirements.txt"):
            print("Failed to install dependencies!")
            return
    
    # Create migrations
    print("\n2. Creating database migrations...")
    if not run_command("python manage.py makemigrations"):
        print("Failed to create migrations!")
        return
    
    # Apply migrations
    print("\n3. Applying database migrations...")
    if not run_command("python manage.py migrate"):
        print("Failed to apply migrations!")
        return
    
    # Create media directory
    print("\n4. Creating media directories...")
    os.makedirs("media/qr_codes", exist_ok=True)
    print("Media directories created.")
    
    print("\n" + "=" * 50)
    print("Setup complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Run the server: python manage.py runserver")
    print("3. Access the application at: http://127.0.0.1:8000/")
    print("\nOptional: Create a .env file with GROQ_API_KEY for AI features")

if __name__ == "__main__":
    main()

