# Password Manager 2.1

## Introduction
This is a basic password manager which has a deafult master password which is used to access the password manager program. We can add, retrieve and generate passwords according to the service which we enter as the input. 

## Features
- **Use of fernet**: The Password Manager uses fernet which is a symmetric encryption algorithms to ensure the security of your passwords.
- **Account Management**: You can easily add and retrieve accounts in the Password Manager.
- **Security of database**: The password json file and the secret key can only be accessied by the admin and will require root access for that.
- **Support of Multi-User Service**: Now we add multiple users of same service and get the respective passwords for the users.
- **Password generator**: This option will help you generate 12 characters which would randomly generated as to ensure prevention of brute-force attack
- **Use of secrets module**: The Password manager uses secrets module which provides functions for generating secure tokens and random numbers, making it suitable for security-sensitive applications.
- **Variable Passwords**: Now we can generate variable-length passwords.  

## Installation
To install the Network Analyzer, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/SwayamRao/password_manager
    ```

2. Change to the project directory:
    ```bash
    cd password_manager
    ```

3. Install the dependencies:
    ```bash
    pip install scapy
    ```

## Usage
1. Clone the reposatory.
2. The default master password is `hello` you can change it.
3. This master password is all that you need to remember.
4. Now there will be options prompted in the program according to that we can add, retrieve and generate passwords and store usernames with respective passwords based on services we give.
5. The files `passwords.json` and `secret.key` can be only accessed by the admin.

## Contact
For any inquiries or support, please contact me at work.mail.g@proton.me 
