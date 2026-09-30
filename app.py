from flask import Flask , jsonify, request

app = Flask(__name__)

students = [
        {"id": 1, "name" : "Sarfaraz", "age" : 30},
        {"id": 2, "name" : "Afsar", "age" : 25},
        {"id": 3, "name" : "Ali", "age" : 26} 
] 


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/students", methods=["GET"])
def get_students():
     return jsonify(students)
 
@app.route("/students/<int:id>",methods=["GET"])
def get_student_id(id):
    for student in students:
        if student["id"] == id:
            return student
    return "Student not found"

@app.route("/students",methods=["POST"])
def add_student():
    add_student_details = request.get_json()
    new_student = {}
    id = len(students) + 1
    new_student["id"] = id
    new_student["name"] = add_student_details.get("name")
    new_student["age"] = add_student_details.get("age")
    students.append(new_student)
    return "Successfully added"

@app.route("/students/<int:id>",methods=["PUT"])
def update_student(id):
    update_student_details = request.get_json()
    for student in students:
        if student["id"] == id:
            if update_student_details.get("name"):
                student["name"] = update_student_details.get("name")
            if update_student_details.get("age"):
                student["age"] = update_student_details.get("age")
            return "Student updated successfully"
    return "Student not found"

@app.route("/students/<int:id>",methods=["DELETE"])
def delete_student(id):
  for student in students:
    if student["id"] == id:
      students.remove(student)
      return "Successfully deleted"
  return "Student not found"

app.run(debug=True)