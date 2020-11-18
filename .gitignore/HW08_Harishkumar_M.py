'''This program will do the methods mentioned in Lab8'''
import unittest
import typing
from typing import Any,List,Iterator, Optional, DefaultDict, Tuple, IO, Dict
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from prettytable import PrettyTable
import os


def date_arithmetic() -> Tuple[datetime, datetime, int]:
    'returns datetime and value for the 3 questions specified in the problem'

    after_feb2020:datetime= datetime.strptime('27 FEB 2019','%d %b %Y') + timedelta(days=3)
    after_feb2019:datetime= datetime.strptime('27 FEB 2020','%d %b %Y') + timedelta(days=3)
    days_passed:datetime= datetime.strptime('30 SEP 2019','%d %b %Y') - datetime.strptime('1 FEB 2019','%d %b %Y')
    return after_feb2020,after_feb2019,days_passed

def file_reader(path:str, fields:int, sep:str=',', header:bool=False) -> Iterator[List[str]]:
    'returns a List of strings for each line in file with their respective fields separated by sep'

    try:
        fp:IO = open(path)
    except FileNotFoundError:
        print(f'File is not present at : {path}')
    else:
        with fp:
            result:str = ""
            split:List[str]= list()
            
            for lineNo,line in enumerate(fp):
                line = line.rstrip('\n')            
                split = line.split(sep,maxsplit=fields)

                if(len(split) != fields):
                    raise ValueError(f'Value ERROR: file_name = {path}; Check line= {lineNo + 1}; No. of Fields = {len(split)}; Expected Fields = {fields}')
                
                if(header):
                    header = False
                    continue

                yield split
                

class FileAnalyzer:
    """ This class will help us to browse through a given directory for .py files and gives it's summary"""
    def __init__(self, directory: str) -> None:
        """ Initialization of attributes"""
        self.directory: str = directory 
        self.files_summary: Dict[str, Dict[str, int]] = dict() 

        self.analyze_files() 

    def analyze_files(self) -> None:
        """ This method will analyze the python file for number of classes,function,lines and characters involved."""

        try:
            fileList:List[Any]= os.listdir(self.directory)
        except FileNotFoundError as e:
            print(f'Directory {self.directory} not found')
        else:  
            cwd = os.getcwd()
            os.chdir(self.directory)
            for filename in fileList:
                if(filename.endswith('.py')):
                    try:
                        fp:IO = open(filename)
                    except FileNotFoundError as e:
                        print(f'File {filename} in directory {self.directory} cannot be opened')
                    else:
                        with fp:
                            fileValues:Dict[str,int] = {'class':0,'func':0,'lines':0,'char':0}
                            for lineNo,line in enumerate(fp):
                                fileValues['lines'] = lineNo + 1
                                fileValues['char'] = fileValues['char'] + len(line)
                                if(line.lstrip().startswith('def ')):
                                    fileValues['func'] = fileValues['func'] + 1
                                if(line.lstrip().startswith('class ')):
                                    fileValues['class'] = fileValues['class'] + 1
                            self.files_summary[filename] = fileValues

            os.chdir(cwd)     

    def pretty_print(self) -> None:
        """ This method will print the file summary in a tabular format."""
        pt: PrettyTable = PrettyTable(field_names=['File Name','Class','Function','Lines','Characters'])
        for key,value in self.files_summary.items():
            filename = key
            classTotal = value['class']
            funcTotal = value['func']
            lineTotal = value['lines']
            charTotal = value['char']
            pt.add_row([filename, classTotal, funcTotal, lineTotal, charTotal])
        print(pt)


def main() -> None:
    'This is the main method for the program'

    print('main check')
    
    print(date_arithmetic())
    
    path = r'testfile_HW08.txt'

    try:
        for cwid, name, major in file_reader(path, 3, sep='|', header=True):  
            print(f"cwid: {cwid} name: {name} major: {major}")        
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    
    try:
        for cwid, name, major in file_reader(r'testfile_HW09.txt', 3, sep='|', header=True):  
            print(f"cwid: {cwid} name: {name} major: {major}")        
    except ValueError as e:
        print(e)

    f1:FileAnalyzer = FileAnalyzer(r'HW08_testfiles')
    f1.pretty_print()

    try:
        for cwid, name, major in file_reader(r'testfile_HW08_1.txt', 3, sep='|', header=True):  
            print(f"cwid: {cwid} name: {name} major: {major}")        
    except ValueError as e:
        print(e)
    
    f1:FileAnalyzer = FileAnalyzer(r'HW09_testfiles')
    print('main done')
    
    

if __name__ == "__main__":
    main()
