import base64
from cryptography.fernet import Fernet
import string
import random

# Define key generation function
def generate_key():
  key = Fernet.generate_key()
  return key

# Function to encrypt password
def encrypt_password(password, key):
  f = Fernet(key)
  encrypted_password = f.encrypt(password.encode())
  return encrypted_password.decode()

# Function to decrypt password
def decrypt_password(encrypted_password, key):
  f = Fernet(key)
  decrypted_password = f.decrypt(encrypted_password.encode()).decode()
  return decrypted_password

# Function to generate random password
def generate_random_password(length, include_uppercase=True, include_lowercase=True,
                             include_numbers=True, include_symbols=True):
  characters = []
  if include_uppercase:
    characters.extend(string.ascii_uppercase)
  if include_lowercase:
    characters.extend(string.ascii_lowercase)
  if include_numbers:
    characters.extend(string.digits)
  if include_symbols:
    characters.extend(string.punctuation)
  return ''.join(random.choice(characters) for _ in range(length))

# Main program loop
def main():
  key = None

  # Check if key file exists
  try:
    with open("key.txt", "rb") as key_file:
      key = key_file.read()
  except FileNotFoundError:
    key = generate_key()
    with open("key.txt", "wb") as key_file:
      key_file.write(key)

  passwords = {}

  while True:
    choice = input("Enter (a)dd, (g)et, (d)elete, (l)ist, (p)assword generator, or (q)uit: ")

    if choice == "a":
      website = input("Enter website name: ")
      password = input("Enter password (or leave blank to generate): ")
      if not password:
        password_length = int(input("Enter desired password length: "))
        password = generate_random_password(password_length)
      encrypted_password = encrypt_password(password, key)
      passwords[website] = encrypted_password
      print("Password added successfully!")

    elif choice == "g":
      website = input("Enter website name: ")
      if website in passwords:
        decrypted_password = decrypt_password(passwords[website], key)
        print(f"Password for {website}: {decrypted_password}")
      else:
        print("Website not found!")

    elif choice == "d":
      website = input("Enter website name: ")
      if website in passwords:
        del passwords[website]
        print("Password deleted successfully!")
      else:
        print("Website not found!")

    elif choice == "l":
      if passwords:
        for website, encrypted_password in passwords.items():
          print(f"Website: {website}")
      else:
        print("No passwords stored!")

    elif choice == "p":
      password_length = int(input("Enter desired password length: "))
      include_uppercase = input("Include uppercase letters (y/n): ").lower() == "y"
      include_lowercase = input("Include lowercase letters (y/n): ").lower() == "y"
      include_numbers = input("Include numbers (y/n): ").lower() == "y"
      include_symbols = input("Include symbols (y/n): ").lower() == "y"
      generated_password = generate_random_password(password_length,
                                                     include_uppercase, include_lowercase,
                                                     include_numbers, include_symbols)
      print(f"Generated password: {generated_password}")

    elif choice == "q":
      break

if __name__ == "__main__":
  main()