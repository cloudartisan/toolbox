#!/usr/bin/env python3

"""
For details on how to create a JWT for a Salesforce Connected App refer to:
https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm&type=5

The expiration time (expressed as the number of seconds from
1970-01-01T0:0:0Z measured in UTC) is assumed to be 3 minutes from
"now".
"""


import argparse
from base64 import urlsafe_b64encode, urlsafe_b64decode
from time import time

# pip install pycryptodomex
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA


# JWT signing algorithms
RS256 = 'RS256'
HS256 = 'HS256'

# Salesforce requires that a JWT is signed using RSA SHA256
DEFAULT_SIGNING_ALGORITHM = RS256

# The Salesforce Connected App client ID, obtained from
# https://git.soma.salesforce.com/chatbots/postman-collections/blob/fe4f7e2b347d224bae6eed5e5b6f1aef638288a1/api/environment/Falcon%20dev1-uswest2%20Env.postman_environment.json#L52
DEFAULT_ISSUER = "3MVG9qKMKuRGRcbtD8wJx6szsQ64vVaBhR1cml9mVJedwgGJGPAmexADroP7qXx3q5lB662oTFe4yKWMU30lE"

# The audience, assumed to be from
# https://git.soma.salesforce.com/chatbots/postman-collections/blob/fe4f7e2b347d224bae6eed5e5b6f1aef638288a1/api/environment/Falcon%20dev1-uswest2%20Env.postman_environment.json#L42
DEFAULT_AUDIENCE = "https://login.stmfb.stm.salesforce.com"

# Complete guess!
DEFAULT_SUBJECT = "chatbot-runtime@salesforce.com"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('private_key_file',
                        type=argparse.FileType('r'),
                        help="Private key file (required)")
    parser.add_argument('public_key_file',
                        nargs='?', type=argparse.FileType('r'),
                        help="Public key file (optional, to verify signature)")
    parser.add_argument('-S', '--signing-algorithm',
                        default=DEFAULT_SIGNING_ALGORITHM)
    parser.add_argument('-i', '--issuer',
                        default=DEFAULT_ISSUER)
    parser.add_argument('-a', '--audience',
                        default=DEFAULT_AUDIENCE)
    parser.add_argument('-s', '--subject',
                        default=DEFAULT_SUBJECT)
    return parser.parse_args()


def get_header_b64(signing_algorithm=DEFAULT_SIGNING_ALGORITHM):
    """
    Returns a base64-encoded ASCII string of the header, suitable for use
    in constructing a JWT.
    """
    header = f'{{"alg":"{signing_algorithm}"}}'
    header_bytes = header.encode()
    header_b64 = urlsafe_b64encode(header_bytes)
    return header_b64.decode()


def get_claim_b64(iss=DEFAULT_ISSUER, sub=DEFAULT_SUBJECT, aud=DEFAULT_AUDIENCE):
    """
    Assumes an expiration 3 minutes from now.

    Returns a base64-encoded ASCII string of the claim set, suitable for use
    in constructing a JWT.
    """
    exp = time() + 180
    claim = f'{{"iss": "{iss}", "sub": "{sub}", "aud": "{aud}", "exp": "{exp}"}}'
    claim_bytes = claim.encode()
    claim_b64 = urlsafe_b64encode(claim_bytes)
    return claim_b64.decode()


def get_signature_b64(private_key, payload):
    key = RSA.import_key(private_key)
    assert key.has_private() == True, "Not a private key"
    assert key.can_sign() == True, "Key not suitable for signing"
    digest = SHA256.new(payload.encode())
    signature = PKCS1_v1_5.new(key).sign(digest)
    signature_b64 = urlsafe_b64encode(signature)
    return signature_b64.decode()


def verify_signature_b64(public_key, payload, signature_b64):
    key = RSA.import_key(public_key)
    digest = SHA256.new(payload.encode())
    signature = urlsafe_b64decode(signature_b64)
    try:
        PKCS1_v1_5.new(key).verify(digest, signature_b64)
    except (ValueError, TypeError):
        print("Failed to verify the signature", file=sys.stderr)


def main():
    args = parse_args()
    header_b64 = get_header_b64(args.signing_algorithm)
    claim_b64 = get_claim_b64(args.issuer, args.subject, args.audience)
    payload = f"{header_b64}.{claim_b64}"
    signature_b64 = get_signature_b64(args.private_key_file.read().strip(), payload)
    if args.public_key_file:
        verify_signature_b64(args.public_key_file.read().strip(), payload, signature_b64)
    jwt = f"{payload}.{signature_b64}"
    print(jwt)


if __name__ == "__main__":
    main()
