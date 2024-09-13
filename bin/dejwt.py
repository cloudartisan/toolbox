"""
dejwt.py

A script for extracting and decoding JWT (JSON Web Token) from any
text input (e.g., logs, command output).  It reads input via stdin,
extracts the first JWT token it finds, and decodes the header and
payload, printing them in a readable JSON format. The signature is
also printed for reference.

Usage:
    - Provide the script with text input containing a JWT via stdin.
    - The script will extract and decode the first valid JWT found.

Example:
    $ echo "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJIZWxsbyB5b3UiLCJuYW1lIjoiV2h5IGFyZSB5b3UgY2hlY2tpbmcgbXkgdG9rZW4_ICggzaHCsCDNnMqWIM2hwrApIiwiaWF0IjoxNTE2MjM5MDIyfQ.yAP0xiTwp6vqIYbLKLVBRv-gTyMvU17rT3H8uErLjHA" | python dejwt.py
    Decoded JWT:
    Header: {
        "alg": "HS256",
        "typ": "JWT"
    }
    Payload: {
        "sub": "Hello you",
        "name": "Why are you checking my token? ( \u0361\u00b0 \u035c\u0296 \u0361\u00b0)",
        "iat": 1516239022
    }
    Signature: yAP0xiTwp6vqIYbLKLVBRv-gTyMvU17rT3H8uErLjHA
"""

import base64
import json
import re
import sys


def base64_url_decode(input_str):
    """
    Decode a base64 string with URL and filename safe alphabet.

    Parameters:
        input_str (str): The base64-encoded string to decode.

    Returns:
        bytes: The decoded bytes.
    """
    padding = '=' * (4 - len(input_str) % 4)
    input_str += padding
    return base64.urlsafe_b64decode(input_str)


def decode_jwt(jwt_token):
    """
    Decode a JWT token into header, payload, and signature.

    Parameters:
        jwt_token (str): The JWT token as a string.

    Returns:
        tuple: Decoded header, payload, and the signature.
    """
    parts = jwt_token.split('.')
    if len(parts) != 3:
        raise ValueError(
            "Invalid JWT structure. Must contain three parts: "
            "header, payload, and signature."
        )

    header_encoded, payload_encoded, signature_encoded = parts

    # Decode the header and payload from base64
    header_json = base64_url_decode(header_encoded).decode('utf-8')
    payload_json = base64_url_decode(payload_encoded).decode('utf-8')

    header = json.loads(header_json)
    payload = json.loads(payload_json)

    return header, payload, signature_encoded


def extract_jwt_from_text(text):
    """
    Extract a JWT token from any text using regex.

    Parameters:
        text (str): The input text from which to extract a JWT token.

    Returns:
        str: The JWT token if found, else None.
    """
    jwt_regex = r'[A-Za-z0-9_-]{2,}(?:\.[A-Za-z0-9_-]{2,}){2}'
    match = re.search(jwt_regex, text)
    if match:
        return match.group(0)
    return None


def main():
    """Main function that reads input, extracts, and decodes the JWT."""
    input_text = sys.stdin.read().strip()

    # Extract the JWT from the input text
    jwt_token = extract_jwt_from_text(input_text)

    if jwt_token:
        try:
            # Decode the JWT
            header, payload, signature = decode_jwt(jwt_token)

            # Output the decoded information
            print("Decoded JWT:")
            print("Header:", json.dumps(header, indent=4))
            print("Payload:", json.dumps(payload, indent=4))
            print("Signature:", signature)

        except ValueError as e:
            print(f"Error decoding JWT: {e}")

    else:
        print("No valid JWT found in the input.")


if __name__ == "__main__":
    main()

