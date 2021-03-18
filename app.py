from flask import Flask, request, render_template, redirect, url_for
import database

# from flask_bootstrap import Bootstrap

app = Flask(__name__)


# Bootstrap(app)

@app.route('/')
def index():
    import pymysql

    db = pymysql.connect(host="localhost", user="root", passwd="c861019", db="free_board")
    cur = db.cursor()

    sql = "SELECT * from board"
    cur.execute(sql)

    data_list = cur.fetchall()

    print(data_list[0])
    print(data_list[1])
    print(data_list[2])

    return render_template('index.html', data_list=data_list)


@app.route('/home2', methods=['GET'])
def home2():
    return render_template('index_example.html')


@app.route('/test', methods=['GET'])
def test():
    return render_template('index_example2.html')


@app.route('/program/<name>')
def program(name):
    return render_template('program.html', name=name)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/make')
def make():
    return render_template('make.html')


@app.route('/input')
def input():
    return render_template('input.html')


@app.route('/apply')
def apply():
    return render_template('apply.html')


@app.route('/applyphoto')
def photo_apply():
    location = request.args.get("location")
    cleaness = request.args.get("clean")
    built_in = request.args.get("built")
    if cleaness == None:
        cleaness = False
    else:
        cleaness = True
    print(location, cleaness, built_in)
    database.save(location, cleaness, built_in)
    return render_template('apply_photo.html')


@app.route('/upload_done', methods=["POST"])
def upload_done():
    upload_files = request.files["file"]
    # print(upload_files)
    upload_files.save("static/assets/img/{}.jpg".format(database.now_index()))
    return redirect(url_for("input"))


@app.route('/list')
def list():
    house_list = database.load_list()
    length = len(house_list)
    print(length,house_list)
    return render_template("list.html", house_list=house_list,length=length)

@app.route('/house_info/<int:index>')
def house_info(index):
    house_info = database.load_house(index)
    location = house_info["location"]
    cleaness = house_info["cleaness"]
    built_in = house_info["built_in"]
    photo=f"assets/img/{index}.jpg"
    print(location, cleaness, built_in,photo)
    return render_template("house_info.html", location=location, cleaness=cleaness, built_in=built_in, photo=photo)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
