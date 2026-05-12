"""
A simple CLI application to view the recent public activities
of a Github account.
"""
# import sys

from urllib.request import Request
from urllib.request import urlopen
import json

my_headers = {"User-Agent": "MyCustomUserAgent/1.0"}
URL = "https://api.github.com/users/sindresorhus/events"

my_req = Request(URL, headers=my_headers)

with urlopen(my_req) as f:
    data = json.load(f)
print(json.dumps(data, indent=2))


# def main():
#     """main func"""
#     if len(sys.argv) > 1:
#         github_url = sys.argv[1]
#     else:
#         print("Enter a url please")
#         return

# if __name__ == "__main__":
#     main()
