# Importing the required package
from flask import Flask, render_template, request
from flasgger import Swagger
import os

# Defining the name (will fetch from the actual file name)
app = Flask(__name__)
Swagger(app)

# Defingin the path or url attahced after the local ip
@app.route('/', methods=['GET'])
# Function that would be executed when the above URL is hit.
def welcome():
    return render_template("index.html")

# Defining second url
@app.route('/name/<your_name>')
# Function that should be executed when this URL is hit
def names(your_name):
    return f"Welcome to Praxis {your_name}"

# Defining Sum 
@app.route("/sum/<no1>,<no2>")
def sum(no1,no2):
    s = float(no1) + float(no2)
    return f"Sum of {no1} and {no2} is {s}"

# Defining Sub 
@app.route("/sub/<no1>,<no2>")
def sub(no1,no2):
    s = float(no1) - float(no2)
    return f"Subtraction of {no1} and {no2} is {s}"

# Defining Mul 
@app.route("/mul/<no1>,<no2>")
def mul(no1,no2):
    s = float(no1) * float(no2)
    return f"Multiplication of {no1} and {no2} is {s}"

# Defining Div 
@app.route("/div/<no1>,<no2>")
def div(no1,no2):
    s = float(no1) / float(no2)
    return f"Division of {no1} and {no2} is {s}"

# # Defining using request
# @app.route('/checking_req',methods=['POST','GET'])
# def get_req_parameters():
#     name = request.args.get("Student_name")
#     roll_no = request.args.get("roll_no")
#     return f"Student name is {name} and roll no is {roll_no} in Praxis",207


# Defining using Swagger
@app.route('/checking_req',methods=['POST','GET'])
def get_req_parameters():
    """ Practicing Swagger
    ---
    parameters:
     - name: Student_name
       in: query
       type: string
       required: true
     - name: roll_no
       in: query
       type: number
       required: true
    responses:
       200:
            description: Result is

    """
    name = request.args.get("Student_name")
    roll_no = request.args.get("roll_no")
    return f"Student name is {name} and roll no is {roll_no} in Praxis"


if __name__ == "__main__":
    # Use debug only when required. With debug no need to stop the server every time.
    app.run()
    #port = int(os.environ.get('PORT',5000))
    #app.run(host='0.0.0.0', port=port)
    # Use Cntl+C to stop the server.