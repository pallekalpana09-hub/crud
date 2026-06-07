from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except:
            return []

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(load_data())

@app.route("/students", methods=["POST"])
def create_student():
    data = load_data()

    student = request.json
    student["result"] = "Pass" if int(student["marks"]) >= 40 else "Fail"

    data.append(student)
    save_data(data)

    return jsonify({"message": "Student Added"})

@app.route("/students/<int:index>", methods=["DELETE"])
def delete_student(index):
    data = load_data()

    if index < len(data):
        data.pop(index)
        save_data(data)

    return jsonify({"message": "Student Deleted"})

if __name__ == "__main__":
    app.run(debug=True)