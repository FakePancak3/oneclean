import os
import time

os.system("")

try:
    from send2trash import send2trash
    has_send2trash = True
except ImportError:
    has_send2trash = False

GREEN = "\033[38;2;39;245;77m"
RED = "\033[38;2;232;69;44m"
GRAY = "\033[90m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

targets = {
    "%TEMP%": [os.environ.get("TEMP", "")],
    "Prefetch": [r"C:\Windows\Prefetch"],
    "Temp": [r"C:\Windows\Temp"],
    "Browser Cache": [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "User Data", "Default", "Cache"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Edge", "User Data", "Default", "Cache"),
    ],
}

selected = {}
for name in targets:
    selected[name] = True

use_recycle_bin = True
skip_recent = True
scan_results = {}

ascii_art = f"""{GREEN}{BOLD}
 ██████╗ ███╗   ██╗███████╗
██╔═══██╗████╗  ██║██╔════╝
██║   ██║██╔██╗ ██║█████╗  
██║   ██║██║╚██╗██║██╔══╝  
╚██████╔╝██║ ╚████║███████╗
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝
{WHITE} ██████╗██╗     ███████╗ █████╗ ███╗   ██╗
██╔════╝██║     ██╔════╝██╔══██╗████╗  ██║
██║     ██║     █████╗  ███████║██╔██╗ ██║
██║     ██║     ██╔══╝  ██╔══██║██║╚██╗██║
╚██████╗███████╗███████╗██║  ██║██║ ╚████║
 ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝
{RESET}"""


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def format_size(num_bytes):
    if num_bytes <= 0:
        return "0 MB"
    mb = num_bytes / (1024 * 1024)
    if mb < 1024:
        return str(round(mb)) + " MB"
    gb = mb / 1024
    return str(round(gb, 2)) + " GB"


def get_folder_size(path):
    total = 0
    if not path or not os.path.exists(path):
        return 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except:
                pass
    return total


def scan_folders():
    print(GREEN + "\nScanning folders...\n" + RESET)
    for name, paths in targets.items():
        size = 0
        for p in paths:
            size += get_folder_size(p)
        scan_results[name] = size
        print(WHITE + name + RESET, "-", GREEN + format_size(size) + RESET)
    time.sleep(1)


def clean_folders():
    names = [n for n in selected if selected[n]]
    if not names:
        print(RED + "\nNo folders selected." + RESET)
        time.sleep(1)
        return

    if not use_recycle_bin:
        confirm = input(RED + "\nSafe Mode is OFF, files will be deleted permanently. Continue? (y/n): " + RESET)
        if confirm.lower() != "y":
            return

    all_files = []
    for name in names:
        for path in targets[name]:
            if not path or not os.path.exists(path):
                continue
            for root, dirs, files in os.walk(path, topdown=False):
                for f in files:
                    all_files.append((name, os.path.join(root, f)))
                for d in dirs:
                    all_files.append((name, os.path.join(root, d)))

    total = len(all_files)
    deleted = 0
    skipped = 0
    freed = 0

    print(GREEN + "\nCleaning...\n" + RESET)

    for i, (name, path) in enumerate(all_files):
        percent = int((i + 1) / total * 100) if total else 100
        print("\r" + GREEN + str(percent) + "%" + RESET + " - " + name + ": " + os.path.basename(path)[:30] + "   ", end="")

        try:
            if os.path.isdir(path):
                os.rmdir(path)
                continue

            if skip_recent:
                mtime = os.path.getmtime(path)
                if time.time() - mtime < 86400:
                    skipped += 1
                    continue

            size = os.path.getsize(path)

            if use_recycle_bin and has_send2trash:
                send2trash(path)
            else:
                os.remove(path)

            freed += size
            deleted += 1

        except:
            skipped += 1

    print("\n\n" + GREEN + "Done." + RESET, "Freed", GREEN + format_size(freed) + RESET, "-", deleted, "deleted,", skipped, "skipped.")
    time.sleep(2)
    scan_folders()


def toggle_folder():
    clear()
    names = list(targets.keys())
    for i, name in enumerate(names):
        mark = GREEN + "x" + RESET if selected[name] else RED + " " + RESET
        print(str(i + 1) + ") [" + mark + "] " + name)

    choice = input(GREEN + "\nEnter number to toggle: " + RESET)
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(names):
            name = names[index]
            selected[name] = not selected[name]


def show_menu():
    clear()
    print(ascii_art)

    print(BOLD + "Folders:" + RESET)
    for name in targets:
        mark = GREEN + "x" + RESET if selected[name] else RED + " " + RESET
        size = ""
        if name in scan_results:
            size = GRAY + " - " + format_size(scan_results[name]) + RESET
        print("[" + mark + "]", name + size)

    if scan_results:
        total = sum(scan_results.values())
        print("\n" + BOLD + "Total space to free: " + RESET + GREEN + format_size(total) + RESET)

    safe_status = GREEN + "ON" + RESET if use_recycle_bin else RED + "OFF" + RESET
    recent_status = GREEN + "ON" + RESET if skip_recent else RED + "OFF" + RESET
    print("\nSafe Mode (Recycle Bin):", safe_status)
    print("Skip files modified in last 24h:", recent_status)

    print(WHITE + "\n1) Scan" + RESET)
    print(WHITE + "2) Toggle folder" + RESET)
    print(WHITE + "3) Toggle Safe Mode" + RESET)
    print(WHITE + "4) Toggle 24h filter" + RESET)
    print(WHITE + "5) Clean" + RESET)
    print(RED + "6) Exit" + RESET)


def main():
    global use_recycle_bin, skip_recent

    while True:
        show_menu()
        choice = input(GREEN + "\nChoose an option: " + RESET)

        if choice == "1":
            scan_folders()
        elif choice == "2":
            toggle_folder()
        elif choice == "3":
            use_recycle_bin = not use_recycle_bin
        elif choice == "4":
            skip_recent = not skip_recent
        elif choice == "5":
            clean_folders()
        elif choice == "6":
            break


main()
