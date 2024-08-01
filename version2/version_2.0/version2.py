import os
import json
import string
import random
from cryptography.fernet import Fernet
from getpass import getpass

def verify_admin():
    master_key = "hello"
    print("*" * 40)
    pro_master_key = getpass("Enter the main password: ")
    if pro_master_key == master_key:
        username = os.getlogin()
        print("Welcome", username)
    else:
        print("Wrong password therefore exiting the program ;)")
        exit()

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
        os.chmod("secret.key", 0o600)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

def add_password(service, username, password, key):
    encrypted_password = encrypt_message(password, key)
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            try:
                passwords = json.load(file)
            except json.JSONDecodeError:
                passwords = {}
    else:
        passwords = {}

    if service not in passwords:
        passwords[service] = []
    
    passwords[service].append({"username": username, "password": encrypted_password.decode()})
    
    with open("passwords.json", "w") as file:
        json.dump(passwords, file, indent=4)

    os.chmod("passwords.json", 0o600)

def get_password(service, key):
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            try:
                passwords = json.load(file)
            except json.JSONDecodeError:
                return None, None
        
        if service in passwords:
            usernames = [entry["username"] for entry in passwords[service]]
            print(f"Usernames for {service}: {', '.join(usernames)}")
            selected_username = input("Enter the username to retrieve the password: ")
            for entry in passwords[service]:
                if entry["username"] == selected_username:
                    encrypted_password = entry["password"].encode()
                    decrypted_password = decrypt_message(encrypted_password, key)
                    return entry["username"], decrypted_password
            return selected_username, None
        else:
            return None, None
    else:
        return None, None

def generate_password(length=12):
    if length < 12:
        raise ValueError("Password length should be at least 12 characters for good security.")

    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation),
    ]
    password += random.choices(all_characters, k=length-4)
    random.shuffle(password)
    return ''.join(password)

if __name__ == "__main__":
    verify_admin()

    if not os.path.exists("secret.key"):
        generate_key()
    key = load_key()
    
    while True:
        print("\nPassword Manager")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            service = input("Enter the service name: ")
            username = input("Enter the username: ")
            gen_password_choice = input("Do you want to generate a strong password? (yes/no): ")
            if gen_password_choice.lower() == 'yes':
                password = generate_password(length=12)
                print(f"Generated password: {password}")
            else:
                password = getpass("Enter the password: ")  
            add_password(service, username, password, key)
            print(f"\nPassword for {service} added successfully.")
        elif choice == "2":
            service = input("Enter the service name: ")
            username, password = get_password(service, key)
            if username and password:
                print(f"Username: {username}")
                print(f"Password: {password}")
            elif username and password is None:
                print(f"No password found for username {username} under service {service}.")
            else:
                print(f"No usernames found for {service}.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")