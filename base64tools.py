class b64():  # Base64 encoder/decoder
    import base64

    def encode(self, data):
        """Encodes the given string using Base64."""
        return self.base64.b64encode(data.encode('utf-8')).decode('utf-8')

    def decode(self, encoded_data):
        """Decodes a Base64 encoded string."""
        return self.base64.b64decode(encoded_data).decode('utf-8')

# Example usage:
if __name__ == "__main__":
    b = b64()
    original_text = "Hello, World!"
    encoded_text = b.encode(original_text)
    decoded_text = b.decode(encoded_text)
    print(f"Original: {original_text}")
    print(f"Encoded: {encoded_text}")
    print(f"Decoded: {decoded_text}")
