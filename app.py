from flask import Flask, render_template, request, jsonify, send_file
import qrcode
from io import BytesIO
import urllib.parse
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    try:
        data = request.get_json()
        upi_id = data.get('upiId', '').strip()
        name = data.get('name', '').strip()
        amount = data.get('amount', '').strip()

        # Validate inputs
        if not upi_id or '@' not in upi_id:
            return jsonify({'error': 'Invalid UPI ID format. Please include @ symbol.'}), 400
        if not name:
            return jsonify({'error': 'Name cannot be empty.'}), 400

        # Construct UPI URL
        params = {
            'pa': upi_id,
            'pn': name,
            'cu': 'INR',
            'tn': 'Payment'
        }

        if amount:
            try:
                float(amount)
                params['am'] = amount
            except ValueError:
                return jsonify({'error': 'Invalid amount format.'}), 400

        # Create UPI URL
        upi_link = "upi://pay?" + urllib.parse.urlencode(params)

        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(upi_link)
        qr.make(fit=True)

        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save image to BytesIO object
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Convert to base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        return jsonify({
            'success': True,
            'upiLink': upi_link,
            'qrCode': f'data:image/png;base64,{img_base64}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)