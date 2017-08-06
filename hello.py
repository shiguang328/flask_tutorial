from flask import Flask, render_template, session, redirect, url_for, flash
from flask import make_response
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment #Flask-Moment 是一个Flask 程序扩展，能把moment.js 集成到Jinja2 模板中。
from datetime import datetime
#表单相关
from flask_wtf import FlaskForm # 以前的Form变成了FlaskForm,新版本中只有FlaskForm了
from wtforms import StringField,SubmitField
from wtforms.validators import Required

# StringField类表示属性为type="text" 的<input> 元素
# SubmitField 类表示属性为type="submit" 的<input> 元素
# 可选参数validators 指定一个由验证函数组成的列表,Required() 确保提交的字段不为空
class NameForm(FlaskForm):
    name = StringField('what is your name?',validators=[Required()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string' #设置Flask-WTF
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app) #初始化Flask Moment

@app.route('/', methods=['GET','POST'])
def index():
    form=NameForm() # NameForm是上面定义的类（继承自flask_wtf.FlaskForm）
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    # 使用get() 获取字典中键对应的值以避免未找到键的异常情况，
    # 因为对于不存在的键，get() 会返回默认值None。
    return render_template('index.html', form=form, name = session.get('name'),
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