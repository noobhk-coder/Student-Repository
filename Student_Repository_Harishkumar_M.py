'''This program will do the functions mentioned in Lab 10'''
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
        self._majors:Dict[str,_Major] = dict()
        self.read_major(os.path.join(self._directory,'majors.txt'))
        self.read_student(os.path.join(self._directory,'students.txt'))
        self.read_instructor(os.path.join(self._directory,'instructors.txt'))
        self.read_grades(os.path.join(self._directory,'grades.txt'))
        

    def read_student(self,path:str)-> None:
        "this method gives call to the file Reader method in HW08 to fill student info "
        try:
            for cwid, name, major in file_reader(path, 3, sep=';', header=True): 
                if major in self._majors: 
                    self._students[cwid] = Student(cwid,name,major,self._majors[major].get_required(),
                                                    self._majors[major].get_electives()) 
                else:
                    print('Major for this student not found: Major name ',major)   
        except (ValueError,FileNotFoundError) as e:
            print(e)
    

    def read_instructor(self,path:str)-> None:
        "this method gives call to the file Reader to fill instructor info "
        try:
            for cwid, name, dept in file_reader(path, 3, sep='|', header=True):  
                self._instructor[cwid] = Instructor(cwid,name,dept)     
        except (ValueError,FileNotFoundError) as e:
            print(e)


    def read_grades(self,path:str)-> None:
        "this method gives call to the file Reader to update course and grade "
        try:
            for std_cwid, course, grade, inst_cwid in file_reader(path, 4, sep='|', header=True): 
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

    def read_major(self,path:str)-> None:
        "this method gives call to the file Reader method in HW08 to fill student info "
        try:
            for major, flag, course in file_reader(path, 3, sep='\t', header=True): 
                if major not in self._majors:
                    self._majors[major] = _Major()
                    self._majors[major].store_major(flag,course)
                else:
                    self._majors[major].store_major(flag,course)
        except (ValueError,FileNotFoundError) as e:
            print(e)

    def table_student(self)->None:
        "this method will print the pretty Table for students"

        pt: PrettyTable = PrettyTable(field_names=['CWID','Name','Major','Completed Courses','Remaining Required',
        'Remaining Electives','GPA'])
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
    
    def table_major(self) -> None:
        """this method will print the pretty Table for Majors"""
        pt: PrettyTable = PrettyTable(field_names=["Major", "Required Courses", "Electives"])
        for majorName in self._majors.keys():
            pt.add_row([majorName, sorted(self._majors[majorName].get_required()), 
            sorted(self._majors[majorName].get_electives())])
        print(pt)


class Student:
    'Holds the student records'
    
    GPA_map:Dict[str,float] = {'A':4.0,'A-':3.75,'B+':3.25,'B':3.0,'B-':2.75,'C+':2.25,'C':2.0,'C-':0,'D+':0,
                                'D':0,'D-':0,'F':0}

    def __init__(self,cwid:str,name:str,major:str,required:List,electives:List) -> None:
        'Creating instances for students'
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = dict()
        self._remaining_required: List[str] = required.copy()
        self._remaining_electives: List[str] = electives.copy()
        self.GPA: float = 0.0
    
    def add_courses(self,course:str,grade:str)->None:
        "this method will add the courses from grades file if the student exist"

        course_GPA = Student.GPA_map.get(grade)
        if(course_GPA != 0):
            self.courses[course] = grade
            if course in self._remaining_required:
                self._remaining_required.remove(course)
            elif course in self._remaining_electives:
                self._remaining_electives.clear()

    def calculate_GPA(self)->None:
        "this method will calculate the GPA for the student"
         
        total_GP:float = 0.0
        course_count:int = 0
        for key,value in self.courses.items():
            total_GP+= Student.GPA_map.get(value,0)
            course_count+=1
        if(course_count != 0):
            self.GPA = round(total_GP / course_count,2)
        

    def Student_table_data(self)->None:
        "this method will provide the data for each student which is required for the pretty table"

        self.calculate_GPA()
        return [self.cwid,self.name,self.major,sorted(self.courses.keys()),self._remaining_required,
        self._remaining_electives,self.GPA]

        
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
    
class _Major:
    """Store data of each Major"""
    def __init__(self):
        """ Initialization for Majors class """
        self._required: List = list()
        self._electives: List = list()

    def store_major(self, flag: str, course: str) -> None:
        """ stores the course for major according to required and elective courses """
        if flag == "R":
            self._required.append(course)
        else:
            self._electives.append(course)

    def get_required(self):
        """return list of required courses"""
        return self._required

    def get_electives(self):
        """return list of elective courses"""
        return self._electives

def main() -> None:
    """
    This is the main method for the program
    here repository of different Universities can be added
    """

    stevens_univ:University = University('Stevens_University_Repository') 
    stevens_univ.table_major() 
    stevens_univ.table_student()
    stevens_univ.table_instructor()
    
    

if __name__ == "__main__":
    main()
