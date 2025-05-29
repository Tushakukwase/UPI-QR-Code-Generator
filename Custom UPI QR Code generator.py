import qrcode
from qrcode.constants import ERROR_CORRECT_L
import os
import urllib.parse

def generate_upi_qr():
    try:
        # Get UPI details from user
        upi_id = input("Enter your UPI ID (e.g., yourname@upi): ").strip()
        name = input("Enter your name/business name: ").strip()
        amount = input("Enter amount (leave empty for any amount): ").strip()
        
        # Validate inputs
        if not upi_id or '@' not in upi_id:
            raise ValueError("Invalid UPI ID format. Please include '@' symbol.")
        if not name:
            raise ValueError("Name cannot be empty.")
            
        # Construct UPI URL with proper parameters
        params = {
            'pa': upi_id,  # Payee address (UPI ID)
            'pn': name,    # Payee name
            'cu': 'INR',   # Currency (Indian Rupee)
            'tn': 'Payment'  # Transaction note
        }
        
        if amount:
            try:
                float(amount)
                params['am'] = amount
            except ValueError:
                print("Warning: Invalid amount format. Amount parameter will be omitted.")
        
        # Create the UPI URL with proper encoding
        upi_link = "upi://pay?" + urllib.parse.urlencode(params)
        
        # Create QR code with custom settings
        qr = qrcode.QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(upi_link)
        qr.make(fit=True)
        
        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        output_file = "upi_payment_qr.png"
        qr_image.save(output_file)
        
        print(f"\nQR Code generated successfully!")
        print(f"Saved as: {os.path.abspath(output_file)}")
        print(f"UPI Link: {upi_link}")
        print("\nTo test the QR code:")
        print("1. Open any UPI payment app (Google Pay, PhonePe, Paytm, etc.)")
        print("2. Scan the generated QR code")
        print("3. Verify the details before making the payment")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("UPI QR Code Generator")
    print("--------------------")
    generate_upi_qr()
