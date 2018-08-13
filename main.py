from cli_parser import parser
import os

def create_x_dirs(x=0, path=None):

    # if the given path 
    if(not os.path.isdir(path)):
        raise NotADirectoryError(path);

    output_path = os.path.join(path,"output");

    # if the output path does not exist, create it
    if(not os.path.isdir(output_path)):
        os.mkdir(output_path)
    
    # create clustered topic directories 
    for i in range(1,x+1):
        name = "topic %d"%i
        new_path = os.path.join(output_path, name)
        os.mkdir(new_path)

def main():

    # parse all the command line arguments
    args = parser.parse_args()

    # validate the path passed in the argument
    if(not os.path.isdir(args.path)):
        raise NotADirectoryError(args.path);

    # create the requried directories
    create_x_dirs(4, args.path)

if __name__ == '__main__':
  main()