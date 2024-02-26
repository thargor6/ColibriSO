# MIT License
#
# ColibriSO - a tool for organizing information of all kinds, written in Python and Streamlit.
# Copyright (C) 2022-2024 Andreas Maschke
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def encrypt_password(password):
    import hashlib
    import hmac
    key = "b1963175-a4be-4096-8d38-53bf19ec"
    byte_key = key.encode("UTF-8")
    message = password.encode()
    h = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return h

def compare_password_hash(password, ref_hash):
    return ref_hash == encrypt_password(password)


import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

def obscure(data: bytes) -> bytes:
    return b64e(zlib.compress(data, 9))

def unobscure(obscured: bytes) -> bytes:
    if obscured is None:
        return None
    return zlib.decompress(b64d(obscured))

def obscure_str(data: str) -> bytes:
    return b64e(zlib.compress(data.encode('utf-8'), 9))

def unobscure_str(obscured: bytes) -> str:
    if obscured is None:
        return None
    return zlib.decompress(b64d(obscured)).decode('utf-8')
