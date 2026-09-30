from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Creating Model
class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    
class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        fields=["id","name","age"]
        load_instance = True    
        
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route("/students",methods=["POST"])
def add_students():
    student_details = request.get_json()
    student= Student(name=student_details["name"],age=student_details["age"])
    db.session.add(student)
    db.session.commit()
    return {'message' : 'Successfully added'}

@app.route("/students",methods=["GET"])
def get_all_students():
    students = Student.query.all()
    return students_schema.dump(students)

@app.route("/students/<int:id>", methods=["GET"])
def get_student_id(id):
    student = Student.query.get(id)
    return student_schema.dump(student)

@app.route("/students/<int:id>",methods=["PUT"])
def update_student(id):
    student = Student.query.get(id)
    updated_details = request.get_json()
    if updated_details.get("name"):
        student.name=updated_details.get("name")
        
    if updated_details.get("age"):
            student.age=updated_details.get("age")
            
    db.session.commit()
            
    return student_schema.dump(student)

@app.route("/students/<int:id>",methods=["DELETE"])
def delete_student(id):
    student=Student.query.get(id)
    
    db.session.delete(student)
    db.session.commit()
    
    return {'message' : 'Successfully deleted'}
    

if __name__ == "__main__":
    app.run(debug = True)