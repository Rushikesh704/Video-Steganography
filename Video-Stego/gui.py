import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from functions import frame_extract, encode_frame, decode_frame
import os
import subprocess

def encrypt_video():
    file_path = filedialog.askopenfilename(title="Select Video File to Encrypt", filetypes=[("Video Files", "*.mp4;*.mov"), ("All Files", "*.*")])
    if file_path:
        try:
            # Extract frames using OpenCV
            frame_extract(os.path.basename(file_path))

            # Encode text into frames
            encode_frame("temp", "data/text-to-hide.txt", int(caesarn_entry.get()))

            # Merge frames back into a video file using ffmpeg
            output_file = os.path.join("data", "encrypted_" + os.path.basename(file_path))
            subprocess.run(['ffmpeg', '-framerate', '25', '-i', os.path.join("temp", "%d.png"), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output_file], capture_output=True, check=True)

            messagebox.showinfo("Success", f"Encryption successful! Encrypted video file saved as '{output_file}'.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e.stderr.decode()}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def decrypt_video():
    caesarn_value = decrypt_caesarn_entry.get().strip()
    if caesarn_value.isdigit():  # Check if input is a valid integer
        caesarn_decrypt = int(caesarn_value)
        file_path = filedialog.askopenfilename(title="Select Video File to Decrypt", filetypes=[("Video Files", "*.mp4;*.mov"), ("All Files", "*.*")])
        if file_path:
            try:
                decode_frame("temp", caesarn_decrypt)
                messagebox.showinfo("Success", "Decryption successful! Recovered text saved as 'recovered-text.txt'.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showerror("Error", "Invalid input. Please enter a valid integer value for Caesar Cipher N.")

# Create main window
root = tk.Tk()
root.title("Caesar Cipher Video Steganography")

# Set window size and make it non-resizable
root.geometry("600x400")
root.resizable(False, False)

# Load background image
background_image = Image.open(r"C:\Users\Acer\Desktop\Work\background.jpg")
background_image = background_image.resize((600, 400), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a label with the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add widgets to encrypt frame
encrypt_frame = tk.Frame(root, bg='white', bd=2)
encrypt_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
encrypt_label = tk.Label(encrypt_frame, text="Encrypt & Merge into Video", bg='white', font=("Helvetica", 14))
encrypt_label.pack(pady=(10, 5))
caesarn_label = tk.Label(encrypt_frame, text="Enter Caesar Cypher N value:", bg='white')
caesarn_label.pack()
caesarn_entry = tk.Entry(encrypt_frame)
caesarn_entry.pack()
encrypt_button = tk.Button(encrypt_frame, text="Encrypt", command=encrypt_video, bg='green', fg='white', width=10, font=("Helvetica", 12))
encrypt_button.pack(pady=(10, 20))

# Add widgets to decrypt frame
decrypt_frame = tk.Frame(root, bg='white', bd=2)
decrypt_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
decrypt_label = tk.Label(decrypt_frame, text="Decrypt & Get the Plain Text", bg='white', font=("Helvetica", 14))
decrypt_label.pack(pady=(10, 5))
decrypt_caesarn_label = tk.Label(decrypt_frame, text="Enter Caesar Cypher N value:", bg='white')
decrypt_caesarn_label.pack()
decrypt_caesarn_entry = tk.Entry(decrypt_frame)
decrypt_caesarn_entry.pack()
decrypt_button = tk.Button(decrypt_frame, text="Decrypt", command=decrypt_video, bg='blue', fg='white', width=10, font=("Helvetica", 12))
decrypt_button.pack(pady=(10, 20))

# Run the main event loop
root.mainloop()
