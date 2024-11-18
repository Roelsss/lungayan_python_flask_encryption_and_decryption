from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

# Initialize Flask application
app = Flask(__name__)

# Generate a key for encryption and decryption
# In a real application, store this key securely (not hardcoded)
key = Fernet.generate_key()
cipher = Fernet(key)


@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Get the plaintext from the request body
    data = request.get_json()
    plaintext = data.get('text', '')

    if not plaintext:
        return jsonify({'error': 'No text provided'}), 400

    # Encrypt the text
    encrypted_text = cipher.encrypt(plaintext.encode())

    # Return the encrypted text
    return jsonify({'encrypted_text': encrypted_text.decode()}), 200


@app.route('/decrypt', methods=['POST'])
def decrypt():
    # Get the encrypted text from the request body
    data = request.get_json()
    encrypted_text = data.get('encrypted_text', '')

    if not encrypted_text:
        return jsonify({'error': 'No encrypted text provided'}), 400

    try:
        # Decrypt the text
        decrypted_text = cipher.decrypt(encrypted_text.encode()).decode()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Return the decrypted text
    return jsonify({'decrypted_text': decrypted_text}), 200


if __name__ == '__main__':
    # Run the application
    app.run(debug=True)