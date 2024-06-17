import os
import json
from cryptography.fernet import Fernet
from getpass import getpass


def verify_admin():
    master_key = "hello"
    print("*" * 40)
    pro_master_key = getpass("Enter the main password ")
    if pro_master_key == master_key:
        username = os.getlogin()
        print("Welcome",username)
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

    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            passwords = json.load(file)
    else:
        passwords = {}

    encrypted_password = encrypt_message(password, key)
    
    passwords[service] = {"username": username, "password": encrypted_password.decode()}

    with open("passwords.json", "w") as file:
        json.dump(passwords, file, indent=4)

    os.chmod("passwords.json",0o600)

def get_password(service, key):
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            passwords = json.load(file)
        
        if service in passwords:
            encrypted_password = passwords[service]["password"].encode()
            decrypted_password = decrypt_message(encrypted_password, key)
            return passwords[service]["username"], decrypted_password
        else:
            return None, None
    else:
        return None, None

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
            password = getpass("Enter the password: ") 
            add_password(service, username, password, key)
            print(f"\nPassword for {service} added successfully.")
        elif choice == "2":
            service = input("Enter the service name: ")
            username, password = get_password(service, key)
            if username:
                print("\n"+"-" * 40)
                print(f"Username: {username}")
                print(f"Password: {password}")
                print("-" * 40)
            else:
                print("\n")
                print("-" * 40)
                print(f"No password found for {service}.")
                print("-" * 40)

        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
