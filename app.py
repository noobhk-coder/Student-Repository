"""This is a program for Flask app run"""
from flask import Flask, render_template
import sqlite3

app:Flask=Flask(__name__)

# DB_File = r"Student_Repository.sqlite"

@app.route('/')
def hello()-> str:
    return render_template('hello.html',
                            title="Hello Page")


@app.route('/student_table')
def student_record():
    _query: str = """select s.Name as Name, s.CWID, g.Course, g.Grade, i.Name as Instructor
                                  from students s
                                    join grades g on s.CWID = g.StudentCWID
                                    join instructors i on g.InstructorCWID = i.CWID
                                  order by s.Name;"""
    try:
        db: sqlite3.Connection = sqlite3.connect("Student_Repository.sqlite")
    except sqlite3.OperationalError as e:
        print(e)
    else:
        data: List[Dict[str, str]] = \
            [{'student': student, 'cwid': cwid, 'course': course, 'grade': grade, 'instructor': instructor}
             for student, cwid, course, grade, instructor in db.execute(_query)]
        db.close()
    return render_template('student_table.html', title='Student Info', valueSent='Student Repository',
                           students=data)

 
app.run(debug=True)