# Automated style checker that runs flake8 instead of having to manually run it in the terminal
import os
import subprocess

def run_flake8():
    """Run flake8 to check the code style."""
    result = subprocess.run(['flake8', '.'], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Style check failed. See details below:")
        print(result.stdout)
        print(result.stderr)
        return False
    else:
        print("All checks passed successfully.")
        return True

if __name__ == '__main__':
    if not os.path.isfile('requirements.txt'):
        print("Installing flake8...")
        subprocess.run(['pip', 'install', 'flake8'])
    
    print("Running style checker...")
    success = run_flake8()
    
    if not success:
        exit(1)
