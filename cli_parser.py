import argparse

# initiate the parser
parser = argparse.ArgumentParser(
        description="Performs the TOPIC MODELNG")

# add required argument
parser.add_argument(
    'path', 
    help="The path to the directory where files are stored"
)