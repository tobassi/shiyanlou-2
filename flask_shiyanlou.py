from flask import Flask
import os,json
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:taoq1992@111.231.140.11/shiyanlou'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#
class File(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80))
    create_time=db.Column(db.DateTime)
    category_id=db.Column(db.Integer,db.ForeignKey('Category.id'))
    content=db.Column(db.Text)
# #
class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))






db.create_all()
java = Category('Java')
python = Category('Python')
file1 = File('Hello Java', datetime.now(), java, 'File Content - Java is cool!')
file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
db.session.add(java)
db.session.add(python)
db.session.add(file1)
db.session.add(file2)
db.session.commit()











base_dir = os.path.dirname(__file__)
files = {}
files_path = os.path.join(base_dir,'files')
files_name = os.listdir(files_path)
for i in files_name:
    path = os.path.join(files_path, i)
    with open(path, 'r') as f:
        a = json.load(f)
        files[os.path.splitext(i)[0]]=a

@app.route('/')
def index():

    return render_template('index.html',files=files)


@app.route('/files/<filename>')
def file(filename):
    a_path = os.path.join(base_dir, 'files',filename+'.json')
    if os.path.exists(a_path):

        return render_template('file.html',file=files[filename])
    else:
        return render_template('404.html'), 404

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404




if __name__ == '__main__':
    app.run()