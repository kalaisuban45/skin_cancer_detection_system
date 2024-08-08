from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import bcrypt
import base64
import os
import uuid
from prediction import Model
app = Flask(__name__)
model__ = Model()


# Connecting to MySQL database
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "skin_users"

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])

def index():
    return render_template('index.html')
@app.route('/detection_tool',methods=['GET','POST'])
def detection_tool():
    if request.method == 'POST':
        tempimage = request.form["img-data"]
        tempimage1 = request.files['img-data-']
        print("tempimage :",tempimage1)
        restemp = tempimage.split(',')[1]
        image_data = base64.b64decode(restemp)
        random_uuid = uuid.uuid4()
        random_string = random_uuid.hex
        imgname = random_string[:5]
        print("imgname :", imgname)
        if tempimage1:
            # tempimage1.save(f'E:\/skin_cancer_detection_sam\static\{imgname}.png')
            tempimage1.save(f'./static/{imgname}.png')
            
        elif tempimage:
            with open(f'./static/{imgname}.png', "wb") as file:
                file.write(image_data)
        result = model__.get_output(f'./static/{imgname}.png')
        # return render_template("web.html", result=result, img_url="static/"+file.filename)
        print("result :",result)
        return render_template('detection_tool.html', class_=result['class'], score=result['score'], predicted=result['predicted'])
    return render_template('detection_tool.html')

@app.route('/disease',methods=['GET','POST'])
def disease():
    return render_template('disease_details.html')

@app.route('/basal_cell',methods=['GET','POST'])
def basal_cell():
    return render_template('basal_cell.html')
@app.route('/aactinic_keratoses',methods=['GET','POST'])
def actinic_keratoses():
    return render_template('actinic_keratoses.html')
@app.route('/benign_keratosisl',methods=['GET','POST'])
def benign_keratosis():
    return render_template('benign_keratosis.html')

@app.route('/dermatofibroma',methods=['GET','POST'])
def dermatofibroma():
    return render_template('dermatofibroma.html')

@app.route('/melanoma',methods=['GET','POST'])
def melanoma():
    return render_template('melanoma.html')

@app.route('/melanocytic-nevi',methods=['GET','POST'])
def melanocyticnevi():
    return render_template('melanocytic-nevi.html')

@app.route('/vascular',methods=['GET','POST'])
def vascular():
    return render_template('vascular.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            # Creating a cursor
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
            mysql.connection.commit()
            cur.close()
            return redirect('/login')
        except Exception as e:
            print(e)
            return "There was an issue adding your data"

    return render_template('reg.html')

@app.route('/benign_keratosis',methods=['GET','POST'])
def begin():
    return render_template('benign_keratosis.html')

@app.route('/actinic_keratoses',methods=['GET','POST'])
def actinic():
    return render_template('actinic_keratoses.html')

@app.route('/limitations',methods=['GET','POST'])
def limitations():
    return render_template('limitations.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Creating a cursor
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", [email])
            user = cur.fetchone()
            cur.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
                session['loggedin'] = True
                session['username'] = user[1]
                return redirect('/')
            else:
                return "Invalid credentials"
        except Exception as e:
            print(e)
            return "There was an issue logging in"

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        return f"Welcome {session['username']}!"
    return redirect(url_for('login'))

@app.route("/get_output", methods=["POST"])
def getoutput():
    # # print(request.form['img-data'])
    tempimage = request.form["img-data"]
    restemp = tempimage.split(',')[1]
    image_data = base64.b64decode(restemp)
    random_uuid = uuid.uuid4()
    random_string = random_uuid.hex
    imgname = random_string[:5]
    with open(f'./static/{imgname}.png', "wb") as file:
        file.write(image_data)
    result = model__.get_output(f'./static/{imgname}.png')
    # return render_template("web.html", result=result, img_url="static/"+file.filename)
    print("result :",result)
    return result['class']
    # # try:
    #     tempimage = request.form["img-data"]
    #     restemp = tempimage.split(',')[1]
    #     image_data = base64.b64decode(restemp)
    #     random_uuid = uuid.uuid4()
    #     random_string = random_uuid.hex
    #     imgname = random_string[:5]
    #     img_path = f'static/{imgname}.png'
    #     full_img_path = os.path.join('E:\\front_end_skin', img_path)

    #     # Ensure the directory exists
    #     os.makedirs(os.path.dirname(full_img_path), exist_ok=True)

    #     # Save the image
    #     with open(full_img_path, "wb") as file:
    #         file.write(image_data)

    #     # Get the result from the model
    #     result = model__.get_output(full_img_path)

    #     # Assuming your static files are served correctly
    #     img_url = f"/{img_path}"

    #     return render_template("web.html", result=result, img_url=img_url)
    # # except FileNotFoundError as e:
    # #     return f"File not found error: {str(e)}"
    # # except Exception as e:
    # #     return f"An error occurred: {str(e)}"
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
