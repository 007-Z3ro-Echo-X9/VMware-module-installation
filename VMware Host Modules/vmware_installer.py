#!/usr/bin/env python3
import os
import subprocess

# Function to run shell commands
def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error occurred: {result.returncode}")
        exit(1)

# Step 1: Install necessary packages
print("Installing required packages...")
run_command("sudo apt update")
run_command("sudo apt install -y build-essential gcc make perl linux-headers-$(uname -r) git")

# Step 2: Clone the repository
print("Cloning VMware host modules repository...")
run_command("git clone https://github.com/mkubecek/vmware-host-modules.git")
os.chdir('vmware-host-modules')
run_command("git checkout workstation-17.5.2")

# Step 3: Apply patches
print("Applying patches...")
files_to_patch = {
    'vmmon-only/common/vmx86.c': 'random_get_entropy_fallback',
    'vmnet-only/bridge.c': 'dev_base_lock'
}

for file_path, error_text in files_to_patch.items():
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            if error_text in content:
                if error_text == 'random_get_entropy_fallback':
                    content = content.replace(error_text, 'random_get_entropy')
                elif error_text == 'dev_base_lock':
                    content = content.replace('read_lock(&dev_base_lock)', 'read_lock(&devnet->dev_base_lock)')
                with open(file_path, 'w') as file:
                    file.write(content)
                print(f"Patch applied to {file_path}")

# Step 4: Build and Install
print("Building and installing VMware modules...")
run_command("make")
run_command("sudo make install")

# Step 5: Load modules
print("Loading VMware modules...")
run_command("sudo modprobe vmmon")
run_command("sudo modprobe vmnet")

print("VMware modules installed and loaded successfully!")
