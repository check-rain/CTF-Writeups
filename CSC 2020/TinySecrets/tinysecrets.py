import gzip
import os
import socketserver
import re

# pip install "cryptography"
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend

flag = os.environ.get("FLAG", "flag{not_the_flag}")

if not re.match(r"flag{[a-z_]+}", flag):
    raise ValueError("Invalid flag format")

flag = flag.encode()  # Convert to bytes
nonce = os.urandom(16)
key = os.urandom(32)
algorithm = algorithms.ChaCha20(key, nonce)
cipher = Cipher(algorithm, mode=None, backend=default_backend())
encryptor = cipher.encryptor()


def compress(src: bytes) -> bytes:
    return gzip.compress(src)


def encrypt(src: bytes) -> bytes:
    return encryptor.update(src)


class FlagServer(socketserver.StreamRequestHandler):
    def handle(self):
        data = self.rfile.readline().strip()
        if data == flag:
            self.wfile.write(flag + b"\n")
            self.finish()
            return

        resp = flag + data
        resp = compress(resp)
        resp = encrypt(resp)
        resp = resp.hex()
        self.wfile.write(resp.encode())
        self.wfile.write(b"\n")
        self.finish()


def main():
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", "1337"), base=10)

    # Create the server, binding to "0.0.0.0" on port 1337
    server = socketserver.TCPServer((HOST, PORT), FlagServer)
    print(f"Listening on TCP {HOST}:{PORT}", flush=True)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


if __name__ == "__main__":
    main()
