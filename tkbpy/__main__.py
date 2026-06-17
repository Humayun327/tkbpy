from .cli import handle_args
import sys

if __name__ == "__main__":
    # Passes whatever you typed after '-m tkbpy' to the CLI logic
    handle_args(sys.argv[1:])