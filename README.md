# User Credentials Manager using Python

<p align="center">
  <img src="https://logos-world.net/wp-content/uploads/2021/10/Python-Symbol.png" width="600" height="300" alt="Python Logo">
</p>

> A secure, menu-driven User Credentials Manager that handles password hashing, encryption, decryption, and periodic key rotation with file-based persistence for credentials and encryption keys.

User Credentials Manager is a secure, menu-driven system for managing user credentials. It uses strong password hashing and encryption to protect sensitive data, with periodic key rotation and automatic re-encryption for enhanced security. Credentials, encryption keys, and timestamps are stored persistently in files. The system allows users to easily add, authenticate, update, and delete accounts, while ensuring data integrity through robust error handling.

## Installing / Getting Started

A quick introduction of the minimal setup you need to get a Hello World up & running in VS Code.

```shell
Install "VS Code" and "Python"
Ensure the "Environment Variable" is included in "the Path" within Python ("Click the Checkbox")
Install the needed "Extensions for VS Code" ["Python by Microsoft, Python Debugger by Microsoft, etc"]
Other Extensions may include ["GitHub, Markdown, Elint/lint, etc"] to utilize GitHub Version Control and other language syntax
Start coding Python
You can run the code by using the following: ["python filename.py"]
```

Congrats! You just created your first "Voice Assistant" file and there's so much more you can do so experiment to your hearts content!

### Initial Configuration

Requirements:
  
- Ensure that the project file/folder and other dependencies you plan to make is within the range for code execution.
  
- Ensure you have a GitHub account to make project repos and save changes to prevent loss of progress with your code in the future.

## Developing

In order to start developing the project further:

```shell
git clone https://github.com/username/project-name.git
cd project-name/
```

After setting up GitHub and the GitHub repo, you should be able to clone/commit/publish your progress as you make changes to the project.

### Building

To build the project after some code changes:

```shell
commit changes by using the GitHub extensions from VS Code or by using the terminal via commands
stash/push the changes into the main/master branch of the project or in another branch if needed
```

After commiting and pushing the changes into GitHub, you should see the project repo change to reflect the most recent code.

### Deploying / Publishing

In case you want to publish your project to a server:

```shell
Ensure that the project is fully functional and give appropiate credit to all contributors/authors.
Provide a step-by-step process of how you managed to complete the project.
Check the project and live server before finalizing the project status.
```

If you want to use GitHub or any other 3rd party platform for your server, you can but it may prove to be difficult with the lack of updated tutorials for all sorts of software services. 
[You can checkout the masterPortfolio repo to see how to use GitHub pages]

## Features

This project repo has the following:

- Core Features:
  - **Encrypt and Decrypt User Data**:
    - Encrypts sensitive data (e.g., usernames, passwords) using **Fernet encryption**.
    - Decrypts data when needed to authenticate or update user credentials.
  - **Password Hashing**:
    - Uses **bcrypt** to hash and verify user passwords securely.    
  - **Persistent Storage**:
    - Stores encrypted user credentials in a **JSON file** (`credentials.json`).
    - Saves the encryption key in a separate **key file** (`encryption.key`).

- User Operations:
  - **Add User**:
    - Allows users to be added to the system with a username and password.
    - Passwords are hashed and stored securely.
  - **Authenticate User**:
    - Verifies user login by comparing the entered password with the hashed password in storage.    
  - **Update User Password**:
    - Allows users to change their password by providing the current username and new password.
    - The new password is hashed and updated in the storage.
  - **Update Username**:
    - Allows users to change their username.
    - Ensures that the new username is not already in use.    
  - **Delete User**:
    - Allows the deletion of a user from the system.

- Key Management:
  - **Encryption Key**:
    - Generates and stores an **encryption key** using **Fernet** if one does not already exist.
    - Uses the key to encrypt and decrypt all sensitive data (e.g., usernames, passwords).
  - **Periodic Key Rotation**:
    - Periodically checks whether the encryption key needs to be rotated (e.g., every 30 days).
    - When key rotation is needed:
      - A new key is generated.
      - All stored data is decrypted with the old key and re-encrypted with the new key.
      - The new key is saved and used for future operations.
  - **Timestamp for Key Rotation**:
    - Stores the timestamp of the last key rotation in a **separate timestamp file** (`key_timestamp.json`).
    - Compares the current time with the timestamp to determine if key rotation is necessary.

- File-based Persistence:
  - **Credentials Storage**:
    - Stores encrypted usernames and hashed passwords in a **JSON file** (`credentials.json`).
    - Each username and password is encrypted before being saved, ensuring security.
  - **Key Storage**:
    - The encryption key is saved in a file (`encryption.key`), so it can be reused across program executions.
  - **Timestamp Storage**:
    - Stores the last key rotation timestamp in a separate JSON file (`key_timestamp.json`).
    - This helps track when the key was last rotated to determine when a new rotation is needed.

- Menu and User Interaction:
  - **Menu-driven Interface**:
    - A simple menu-driven interface allows users to:
      - Add, authenticate, update, or delete users.
      - Perform all actions via the console input.  
  - **User-friendly Prompts**:
    - Prompts the user to enter necessary information (e.g., username, password) to perform actions.
    - Provides feedback after each action (e.g., successful addition, authentication failure, etc.).

- Error Handling:
  - **Checks for Existing Users**:
    - Prevents adding duplicate users with the same username.
    - Ensures the new username is not already in use when updating a username.
  - **Error Messages**:
    - Displays relevant error messages if an action fails (e.g., incorrect password, user not found).

- Security Features:
  - **Strong Encryption and Hashing**:
    - Uses **Fernet** for encryption and **bcrypt** for password hashing, both of which are considered secure and standard for modern applications.  
  - **Data Integrity**:
    - Ensures that encrypted data is stored securely and can only be accessed by decrypting with the correct encryption key.
  
- Extensibility:
  - **Customizable Rotation Interval**:
    - The key rotation interval (currently set to 30 days) can be easily modified in the `check_key_rotation()` function.    
  - **Easily Adaptable for More Features**:
    - The system can be extended to support additional features, such as user role management, multi-factor authentication, etc.

## Links

Helpful links that you can use with your project:

- GitHub Commands Cheat Sheet: [https://github.com/tiimgreen/github-cheat-sheet]
- In case of sensitive bugs like security vulnerabilities, please use the issue tracker or contact me directly. 
  We value your effort to improve the security and privacy of this project!

## References

"Give Credit where its Due": Credit goes to all the original repo owners, contributors, and author into making this project.
(If possible, please provide the GitHub URLs and names to all that contributed including the project owner)

<!-- - "Title" by Author [Social Media/Location] -->

## Licensing

![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)
![cc-by-nc-sa-image](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)

"The code in this project is licensed under Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA) License."