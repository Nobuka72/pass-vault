import string as s
import secrets

def create_password(length: int, symbols: bool, uppercase: bool):
    # Define the base character set
    combination = s.ascii_lowercase + s.digits + s.punctuation 

    #Length check
    if length <= 0:
            raise ValueError("Length must be a positive integer")
    # Add uppercase letters if specified
    if uppercase:
        combination += s.ascii_uppercase
    # Add punctuation if specified
    if symbols:
        combination += s.punctuation 

    password = ''.join(combination[secrets.randbits(12)%len(combination)] for _ in range(length))
    return password

# # # User input

# def generate_password():
#     try:
#         password_length = int(password_length_entry.get())
#         include_symbols = symbols_var.get()
#         include_uppercase = uppercase_var.get()
        
#         generated_password = create_password(password_length, include_symbols, include_uppercase)
#         output_text.delete(1.0, tk.END)  # Clear previous outputs
#         output_text.insert(tk.END, f"Generated Password: {generated_password}\n")

#     except ValueError as e:
#         messagebox.showerror("Input Error", str(e))