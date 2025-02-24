import cv2
import os
import numpy as np

# Load the image
img_path = r"C:\Users\bhara\Downloads\Stenography-main\Stenography-main\1.jpg"
img = cv2.imread(img_path)

if img is None:
    print("Error: Image not found. Check the file path.")
    exit()

# Get image dimensions
height, width, _ = img.shape

msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Convert message to binary
binary_msg = ''.join(format(ord(char), '08b') for char in msg)
binary_msg += '1111111111111110'  # End-of-message delimiter (16 bits)

data_index = 0
msg_length = len(binary_msg)

# Encrypt message into image
for row in range(height):
    for col in range(width):
        for channel in range(3):  # Iterate over R, G, B channels
            if data_index < msg_length:
                pixel_bin = format(img[row, col, channel], '08b')
                new_pixel_bin = pixel_bin[:-1] + binary_msg[data_index]  # Modify LSB
                img[row, col, channel] = int(new_pixel_bin, 2)
                data_index += 1

# Save the encrypted image
encrypted_path = "encryptedImage.png"
cv2.imwrite(encrypted_path, img)
os.system(f"start {encrypted_path}")  # Open the image

# Reload the encrypted image for decryption
img = cv2.imread(encrypted_path)

# Decryption
decrypt_password = input("Enter passcode for Decryption: ")
if decrypt_password == password:
    binary_msg = ""
    for row in range(height):
        for col in range(width):
            for channel in range(3):
                binary_msg += format(img[row, col, channel], '08b')[-1]

    # Extract message
    chars = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]
    message = ""
    for i in range(len(chars) - 1):
        if chars[i] == '11111111' and chars[i+1] == '11111110':  # End of message
            break
        message += chr(int(chars[i], 2))

    print("Decrypted message:", message)
else:
    print("YOU ARE NOT AUTHORIZED")
