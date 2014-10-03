import sys

def _parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    return parser.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    sys.exit(0)
