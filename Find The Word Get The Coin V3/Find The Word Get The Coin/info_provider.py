from colorama import init, Fore
init(autoreset=True)

def SUCCESS(msg):
    print(Fore.GREEN + "[SUCCESS] " + msg)

def ERROR(msg):
    print(Fore.RED + "[ERROR] " + msg)

def INFO(msg):
    print(Fore.BLUE + "[INFO] " + msg)

def WARN(msg):
    print(Fore.YELLOW + "[WARNING] " + msg)