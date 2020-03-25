import pandas as pd
def read_convert_file():

    with open("./1w.txt",'r') as f:
        f.write("hi\n")
        f.write('hwll\n')
def write_file():

    with open("./test.csv",'w') as f:
        f.write("a,b,c")

if __name__ == '__main__':
   write_file()