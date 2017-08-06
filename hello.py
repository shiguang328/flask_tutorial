from flask import Flask, render_template
from flask import make_response
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment #Flask-Moment 是一个Flask 程序扩展，能把moment.js 集成到Jinja2 模板中。
from datetime import datetime
#表单相关
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

# StringField类表示属性为type="text" 的<input> 元素
# SubmitField 类表示属性为type="submit" 的<input> 元素
# 可选参数validators 指定一个由验证函数组成的列表,Required() 确保提交的字段不为空
class NameForm(Form):
    name = StringField('what is your name?',validators=[Required()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string' #设置Flask-WTF
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app) #初始化Flask Moment

@app.route('/')
def index():
    return render_template('index.html',
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
    #manager.run()
    app.run(debug=True)