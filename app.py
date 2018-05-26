from flask import Flask
import os,json
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/shiyanlou'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#
class File(db.Model):
    __tablename__='File'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80))
    create_time=db.Column(db.DateTime)
    category_id=db.Column(db.Integer,db.ForeignKey('Category.id'))
    content=db.Column(db.Text)
# #
class Category(db.Model):
    __tablename__='Category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))




# file1 = File(title='Hello Python', create_time=datetime.now(), category_id=python.id, content='File Content - Python is cool!')
# file2 = File(title='Hello Java', create_time=datetime.now(), category_id=python.id, content='File Content - Java is cool!')




@app.route('/')
def index():
    files = File.query.all()
    # a = File.query.all()
    # for i in a:
    #     a.append([i.id,i.title])
    return render_template('index.html',files=files)


@app.route('/files/<file_id>')
def file(file_id):

    file = File.query.filter_by(id=file_id).first()
    cate = Category.query.filter_by(id=file.id).first()
    file_content={'content':file.content,'time':file.create_time,'category_name':cate.name}
    if file:
        return render_template('file.html',file_content=file_content)
    else :
        return render_template('404.html'),404
#
#
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404




if __name__ == '__main__':
    app.run()

