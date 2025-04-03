from simple_term_menu import TerminalMenu
import os
import json

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def write_to_json(attack_type, attack_subtype):
    data={
        "attack_type": attack_type,
        "attack_subtype": attack_subtype
    }
    with open('info.json', 'w') as json_file:
        json.dump(data, json_file)

def select_attack():
    cls()
    attack_types = [
        "Man in the Middle (MITM)",
        "Denial of Service (DoS)",
        "Scanning",
        "Mirai Botnet"
    ]
    
    attack_subtypes = {
        "Man in the Middle (MITM)": ["ARP Spoofing"],
        "Denial of Service (DoS)": ["SYN Flooding"],
        "Scanning": ["Host Discovery", "Port Scanning", "OS/Version Detection"],
        "Mirai Botnet": ["UDP Flooding", "ACK Flooding", "HTTP Flooding", "Telnet Bruteforce", "Host Discovery"]
    }

    terminal_menu = TerminalMenu(
        attack_types,
        title="Select Attack",
        menu_cursor="-> ",
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("bg_cyan","fg_black"),
    )

    type_index = terminal_menu.show()
    if type_index is None:  # User pressed Esc or Ctrl+C
        raise KeyboardInterrupt
    
    selected_type = attack_types[type_index]
    cls()

    subtypes = attack_subtypes[selected_type]
    terminal_menu = TerminalMenu(
        subtypes,
        title=f"{selected_type} attack's:",
        menu_cursor="→ ",
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("bg_cyan","fg_black"),
    )
    
    subtype_index = terminal_menu.show()
    if subtype_index is None:  # User pressed Esc or Ctrl+C
        raise KeyboardInterrupt

    
    cls()
    selected_subtype = subtypes[subtype_index]
    try:
        write_to_json(selected_type, selected_subtype)
    except Exception as e:
        print(f"Error writing to JSON: {e}")
        raise Exception
