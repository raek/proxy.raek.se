import sys

import gunicorn.app.wsgiapp


def main():
    sys.argv = [
        sys.argv[0].replace("proxy_raek_se", "gunicorn"),
        "--access-logfile", "-",
        "-b", "localhost:4096",
        "proxy_raek_se.app:app",
    ]
    print(sys.argv)
    gunicorn.app.wsgiapp.run()
