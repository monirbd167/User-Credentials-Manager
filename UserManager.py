import json
import bcrypt
import time
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

class UserCredentialsManager:
    def __init__(self, credentials_file='credentials.json', key_file='encryption.key', timestamp_file='key_timestamp.json'):
        self.credentials_file = credentials_file
        self.key_file = key_file
        self.timestamp_file = timestamp_file
        
        # Load or generate encryption key
        self.key = self.load_or_generate_key()
        self.fernet = Fernet(self.key)
        
        # Load or initialize credentials storage
        self.credentials = self.load_credentials()

        # Check if key rotation is needed
        self.check_key_rotation()

    def load_or_generate_key(self):
        """Load encryption key from file or generate a new one."""
        try:
            with open(self.key_file, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key

    def load_key_timestamp(self):
        """Load timestamp of the last key rotation from file."""
        try:
            with open(self.timestamp_file, 'r') as f:
                return json.load(f).get('last_rotation', None)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save_key_timestamp(self):
        """Save the current timestamp as the last rotation time."""
        timestamp = {'last_rotation': time.time()}
        with open(self.timestamp_file, 'w') as f:
            json.dump(timestamp, f)

    def load_credentials(self):
        """Load credentials from a JSON file."""
        try:
            with open(self.credentials_file, 'r') as f:
                encrypted_data = json.load(f)
            # Decrypt each entry
            return {self.decrypt(key): self.decrypt(value) for key, value in encrypted_data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_credentials(self):
        """Save encrypted credentials to the file."""
        encrypted_data = {self.encrypt(key): self.encrypt(value) for key, value in self.credentials.items()}
        with open(self.credentials_file, 'w') as f:
            json.dump(encrypted_data, f)

    def encrypt(self, data):
        """Encrypt data using Fernet encryption."""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        """Decrypt data using Fernet decryption."""
        return self.fernet.decrypt(encrypted_data.encode()).decode()

    def hash_password(self, password):
        """Hash a password using bcrypt with a salt."""
        # bcrypt automatically salts the password for you
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed_password.decode()

    def verify_password(self, hashed_password, password):
        """Verify a hashed password using bcrypt."""
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def add_user(self, username, password):
        """Add a new user to the credentials manager."""
        if username in self.credentials:
            print(f"User {username} already exists.")
            return
        
        hashed_password = self.hash_password(password)
        self.credentials[username] = hashed_password
        self.save_credentials()
        print(f"User {username} added successfully.")

    def update_password(self, username, new_password):
        """Update a user's password."""
        if username not in self.credentials:
            print(f"User {username} does not exist.")
            return
        
        hashed_password = self.hash_password(new_password)
        self.credentials[username] = hashed_password
        self.save_credentials()
        print(f"Password for {username} updated successfully.")

    def update_username(self, old_username, new_username):
        """Update a user's username."""
        if old_username not in self.credentials:
            print(f"User {old_username} does not exist.")
            return

        if new_username in self.credentials:
            print(f"User {new_username} already exists.")
            return

        self.credentials[new_username] = self.credentials.pop(old_username)
        self.save_credentials()
        print(f"Username {old_username} changed to {new_username}.")

    def delete_user(self, username):
        """Delete a user from the credentials manager."""
        if username in self.credentials:
            del self.credentials[username]
            self.save_credentials()
            print(f"User {username} deleted successfully.")
        else:
            print(f"User {username} not found.")

    def authenticate_user(self, username, password):
        """Authenticate a user based on username and password."""
        if username in self.credentials:
            hashed_password = self.credentials[username]
            if self.verify_password(hashed_password, password):
                print(f"Authentication successful for {username}.")
                return True
            else:
                print(f"Authentication failed for {username}. Incorrect password.")
        else:
            print(f"User {username} not found.")
        return False

    def check_key_rotation(self):
        """Check if key rotation is needed based on the last rotation timestamp."""
        last_rotation = self.load_key_timestamp()
        if not last_rotation:
            # No previous rotation, set a timestamp for the first time
            self.save_key_timestamp()
            return
        
        # Define key rotation interval (e.g., 30 days)
        rotation_interval = timedelta(days=30)
        last_rotation_time = datetime.fromtimestamp(last_rotation)
        current_time = datetime.now()

        if current_time - last_rotation_time >= rotation_interval:
            print("Key rotation is needed. Rotating key...")
            self.rotate_key()

    def rotate_key(self):
        """Perform key rotation: decrypt all data with the old key and re-encrypt with the new key."""
        old_key = self.key
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

        # Decrypt all credentials and re-encrypt them with the new key
        old_credentials = self.credentials.copy()
        self.credentials = {}
        
        for username, hashed_password in old_credentials.items():
            decrypted_username = self.decrypt(username)
            decrypted_password = self.decrypt(hashed_password)
            encrypted_username = self.encrypt(decrypted_username)
            encrypted_password = self.encrypt(decrypted_password)
            self.credentials[encrypted_username] = encrypted_password
        
        # Save the new credentials and timestamp
        self.save_credentials()
        self.save_key_timestamp()

        print("Key rotation completed successfully.")

def show_menu():
    """Display the main menu."""
    print("\nUser Credentials Manager")
    print("1. Add User")
    print("2. Authenticate User")
    print("3. Update Password")
    print("4. Update Username")
    print("5. Delete User")
    print("6. Exit")

def main():
    """Run the menu-driven user credentials manager."""
    manager = UserCredentialsManager()

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            manager.add_user(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            manager.authenticate_user(username, password)
        elif choice == '3':
            username = input("Enter username: ")
            new_password = input("Enter new password: ")
            manager.update_password(username, new_password)
        elif choice == '4':
            old_username = input("Enter old username: ")
            new_username = input("Enter new username: ")
            manager.update_username(old_username, new_username)
        elif choice == '5':
            username = input("Enter username to delete: ")
            manager.delete_user(username)
        elif choice == '6':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()