'''This program will do the functions mentioned in Lab 09'''
import unittest
import typing
from typing import Any,List,Iterator, Optional, DefaultDict, Tuple, IO, Dict
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from prettytable import PrettyTable
from HW08_Harishkumar_M import file_reader
import os
                
class University:
    """
    Holds all records of students,instructors and grades
    of a particular university
    """

    def __init__(self,directory:str)-> None:
        "perform initalization and call file reader"
        self._directory = directory
        self._students:Dict[str,Student] = dict()
        self._instructor:Dict[str,Instructor] = dict()
        self.read_student(os.path.join(self._directory,'students.txt'))
        self.read_instructor(os.path.join(self._directory,'instructors.txt'))
        self.read_grades(os.path.join(self._directory,'grades.txt'))

    def read_student(self,path:str)-> None:
        "this method gives call to the file Reader method in HW08 to fill student info "
        try:
            for cwid, name, major in file_reader(path, 3, sep='\t', header=False):  
                self._students[cwid] = Student(cwid,name,major)     
        except (ValueError,FileNotFoundError) as e:
            print(e)
    

    def read_instructor(self,path:str)-> None:
        "this method gives call to the file Reader to fill instructor info "
        try:
            for cwid, name, dept in file_reader(path, 3, sep='\t', header=False):  
                self._instructor[cwid] = Instructor(cwid,name,dept)     
        except (ValueError,FileNotFoundError) as e:
            print(e)


    def read_grades(self,path:str)-> None:
        "this method gives call to the file Reader to update course and grade "
        try:
            for std_cwid, course, grade, inst_cwid in file_reader(path, 4, sep='\t', header=False): 
                try:
                    self._students[std_cwid].add_courses(course,grade) 
                except KeyError as e:
                    print('Student with ID ',e,' not found')                                 
                try:
                    self._instructor[inst_cwid].add_courses_info(course,std_cwid)
                except KeyError as e:
                    print('Instructor with ID ',e,' not found')
        except (ValueError,FileNotFoundError) as e:
            print(e)

    def table_student(self)->None:
        "this method will print the pretty Table for students"

        pt: PrettyTable = PrettyTable(field_names=['CWID','Name','Completed Courses'])
        for key in self._students.keys():
            pt.add_row((self._students[key].Student_table_data()))
        print(pt)
    
    def table_instructor(self)->None:
        "this method will print the pretty Table for Instructors"
        pt: PrettyTable = PrettyTable(field_names=['CWID','Name','Dept','Course','Students'])
        for key in self._instructor.keys():
            for record in self._instructor[key].Instructor_table_data():
                pt.add_row(record)
        print(pt)


class Student:
    'Holds the student records'
    def __init__(self,cwid:str,name:str,major:str) -> None:
        'Creating instances for students'
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = dict()
    
    def add_courses(self,course:str,grade:str)->None:
        "this method will add the courses from grades file if the student exist"
        self.courses[course] = grade

    def Student_table_data(self)->None:
        "this method will provide the data for each student which is required for the pretty table"
        return self.cwid,self.name,sorted(self.courses.keys()) 

        
class Instructor:
    'Holds the instructor records'
    def __init__(self,cwid:str,name:str,dept:str)-> None:
        'Creating instances for instructor'
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.courses:DefaultDict[list] = defaultdict(list)
    
    def add_courses_info(self,course:str,std_cwid:str)->None:
        "this method will add the courses from grades file if the student exist"
        self.courses[course].append(std_cwid)

    def Instructor_table_data(self)->None:
        "this method will provide the data for each student which is required for the pretty table"
        instructor_data: List = list()
        for key, value in self.courses.items():
            instructor_data.append([self.cwid, self.name, self.dept, key, len(value)])
        return instructor_data
    


def main() -> None:
    """
    This is the main method for the program
    here repository of different Universities can be added
    """

    stevens_univ:University = University('Stevens_University_Repository')  
    stevens_univ.table_student()
    stevens_univ.table_instructor()
    

if __name__ == "__main__":
    main()
