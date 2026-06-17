import sys
from .cli import handle_args

if __name__ == "__main__":
    handle_args(sys.argv[1:])