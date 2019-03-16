from flask import Flask, render_template, session, redirect
from login import LoginForm, RegForm
from models import DB, UserModel, NewsModel, CommunityModel


app = Flask(__name__)
app.config['SECRET_KEY'] = 'polina_secret_key'
db = DB()

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    print(session)
    form = LoginForm()
    user_name = form.username.data
    password = form.password.data
    user_model = UserModel(db.get_connection())
    user_model.init_table()
    exists = user_model.exists(user_name, password)
    existence = ''
    if (exists[0]):
        session['username'] = user_name
        session['user_id'] = exists[1]
        return redirect("/news_feed")
    elif not(user_name is None) and not(password is None):
        existence = 'Такого пользователя не существует'
    return render_template('login.html', form=form, existence=existence)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')

@app.route('/registration', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    user_name = form.username.data
    password = form.password.data
    user_model = UserModel(db.get_connection())
    existence = ''
    if not user_name in [tuply[1] for tuply in user_model.get_all()]:
        user_model.insert(user_name, password)
        return redirect("/login")
    elif not (user_name is None) and not (password is None):
        existence = 'Это имя уже занято'
    return render_template('registration.html', form=form, existence=existence)



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')