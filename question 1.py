def encrypt(text, n, m):
    encrypted_text = ""
    for char in text:
        if 'a' <= char <= 'm':
            encrypted_char = chr(((ord(char) - ord('a') + n * m) % 13) + ord('a'))
        elif 'n' <= char <= 'z':
            encrypted_char = chr(((ord(char) - ord('n') - (n + m)) % 13) + ord('n'))
        elif 'A' <= char <= 'M':
            encrypted_char = chr(((ord(char) - ord('A') - n) % 13) + ord('A'))
        elif 'N' <= char <= 'Z':
            encrypted_char = chr(((ord(char) - ord('N') + m**2) % 13) + ord('N'))
        else:
            encrypted_char = char
        encrypted_text += encrypted_char
    return encrypted_text

def decrypt(text, n, m):
    decrypted_text = ""
    for char in text:
        if 'a' <= char <= 'm':
            decrypted_char = chr(((ord(char) - ord('a') - n * m + 13) % 13) + ord('a'))
        elif 'n' <= char <= 'z':
            decrypted_char = chr(((ord(char) - ord('n') + (n + m) + 13) % 13) + ord('n'))
        elif 'A' <= char <= 'M':
            decrypted_char = chr(((ord(char) - ord('A') + n + 13) % 13) + ord('A'))
        elif 'N' <= char <= 'Z':
            decrypted_char = chr(((ord(char) - ord('N') - m**2 + 13) % 13) + ord('N'))
        else:
            decrypted_char = char
        decrypted_text += decrypted_char
    return decrypted_text

def check_decryption(original_text, decrypted_text):
    return original_text == decrypted_text

def main():
    try:
        with open("raw_text.txt", "r") as file:
            original_text = file.read()
    except FileNotFoundError:
        print("Error: raw_text.txt not found.")
        return

    try:
        n = int(input("Enter the value of n: "))
        m = int(input("Enter the value of m: "))
    except ValueError:
        print("Invalid input. Please enter integers for n and m.")
        return
    
    encrypted_text = encrypt(original_text, n, m)

    with open("encrypted_text.txt", "w") as file:
        file.write(encrypted_text)

    print("Text encrypted and saved to encrypted_text.txt")

    decrypted_text = decrypt(encrypted_text, n, m)
    
    with open("decrypted_text.txt", "w") as file:
        file.write(decrypted_text)
    print("Text decrypted and saved to decrypted_text.txt")

    if check_decryption(original_text, decrypted_text):
        print("Decryption successful. Decrypted text matches original text.")
    else:
        print("Decryption failed. Decrypted text does not match original text.")
        print("Original Text:", original_text)
        print("Decrypted Text:", decrypted_text)

if __name__ == "__main__":
    main()