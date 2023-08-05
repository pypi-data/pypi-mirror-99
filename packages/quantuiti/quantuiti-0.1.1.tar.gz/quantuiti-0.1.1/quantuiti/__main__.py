import argparse
import os
def main():
    parser = argparse.ArgumentParser(prog ='quantuiti', 
                                    description ='Quantuiti is a platform designed for automated trading .') 
  
    parser.add_argument('-publish', dest ='publish',  
                        help ='publish algorithm to quantuiti.com') 
  
    args = parser.parse_args() 
  
    if args.publish:
        script_path = args.publish
        try:
            with open(script_path, 'r') as file:
                lines = file.readlines()
                print(lines)
        except FileNotFoundError:
            parser.error(f'FILE {script_path} NOT FOUND')
       
  
if __name__ == "__main__":
    main()