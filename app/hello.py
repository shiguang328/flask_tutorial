from flask import Flask, render_template, session, redirect, url_for, flash
from flask import make_response
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment #Flask-Moment 是一个Flask 程序扩展，能把moment.js 集成到Jinja2 模板中。
from datetime import datetime
import os
from flask_wtf import FlaskForm # 以前的Form变成了FlaskForm,新版本中只有FlaskForm了
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


# StringField类表示属性为type="text" 的<input> 元素
# SubmitField 类表示属性为type="submit" 的<input> 元素
# 可选参数validators 指定一个由验证函数组成的列表,Required() 确保提交的字段不为空
class NameForm(FlaskForm):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'  # 设置Flask-WTF

# mail 相关配置
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)  # 初始化Flask Moment
mail = Mail(app)

# 数据库相关
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 每次请求结束后都会自动提交数据库中的变动
db = SQLAlchemy(app)  # db对象是SQLAlchemy 类的实例，表示程序使用的数据库，同时还获得了Flask-SQLAlchemy提供的所有功能

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 传给db.ForeignKey() 的参数'roles.id' 表明，这列的值是roles 表中行的id 值

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['GET','POST'])
def index():
    form=NameForm() # NameForm是上面定义的类（继承自flask_wtf.FlaskForm）
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name']=form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    # 使用get() 获取字典中键对应的值以避免未找到键的异常情况，
    # 因为对于不存在的键，get() 会返回默认值None。
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known',False),
                           current_time=datetime.utcnow()) #current_time属于moment类

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

if __name__ =='__main__':
    manager.run()
    #app.run(debug=True)