from contextlib import contextmanager
import socket
import ssl

from gemurl import normalize_url, host_port_pair_from_url


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2


@contextmanager
def fetch_bytes(url):
    url = normalize_url(url)
    address = host_port_pair_from_url(url)
    host, port = address
    with socket.create_connection(address) as s:
        with ssl_context.wrap_socket(s, server_hostname=host) as ss:
            # Gemini allows UTF-8 here, but normalized URLs are always ASCII-only
            ss.sendall(f"{url}\r\n".encode("us-ascii"))
            f = ss.makefile("rb")
            header = f.readline().decode("utf-8").strip()
            status, meta = header.split(" ", maxsplit=1)
            status = int(status)
            assert (20 <= status) and (status <= 29), "Status was not 2x SUCCESS"
            mime_type = meta
            if mime_type.startswith("text/") and "charset" not in mime_type:
                mime_type += "; charset=utf-8"
            yield mime_type, f


def main():
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    with fetch_bytes(args.url) as (mime_typ, f):
        sys.stdout.buffer.write(f.read())
