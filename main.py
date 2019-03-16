from flask import Flask, render_template, session, redirect
from forms import LoginForm, RegForm, EditForm
from models import DB, UserModel, NewsModel, CommunityModel


app = Flask(__name__)
app.config['SECRET_KEY'] = 'polina_secret_key'
db = DB()
user_model = UserModel(db.get_connection())
user_model.init_table()
news_model = NewsModel(db.get_connection())
news_model.init_table()

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session:
        return redirect('/login')
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
        #return redirect("/news_feed")
        return redirect(("/profile/{}").format(user_name))
    elif not(user_name is None) and not(password is None):
        existence = 'Wrong username or password'
    return render_template('login.html', form=form, existence=existence)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')

@app.route('/registration', methods=['GET', 'POST'])
def reg():
    if 'username' not in session:
        return redirect('/login')
    form = RegForm()
    user_name = form.username.data
    password = form.password.data
    user_model = UserModel(db.get_connection())
    existence = ''
    if not user_name in [tuply[1] for tuply in user_model.get_all()]:
        user_model.insert(user_name, password)
        return redirect("/login")
    elif not (user_name is None) and not (password is None):
        existence = 'This name is taken'
    return render_template('registration.html', form=form, existence=existence)


@app.route('/profile/<user_name>', methods=['GET', 'POST'])
def profile(user_name):
    if 'username' not in session:
        return redirect('/login')
    user_id = session['user_id']
    news = NewsModel(db.get_connection()).get_all(user_id)
    return render_template('profile.html', user_name=session['username'], news=news)

@app.route('/edit/<user_name>', methods=['GET', 'POST'])
def edit(user_name):
    if 'username' not in session:
        return redirect('/login')
    form = EditForm()
    if session['username'] != user_name:
        return redirect('/profile/<user_name>')
    user_model = UserModel(db.get_connection())
    new_name = form.username.data
    print([tuply[1] for tuply in user_model.get_all()])
    if not new_name in [tuply[1] for tuply in user_model.get_all()]:
        user_model.update(new_name, session['user_id'])
        session['username'] = new_name
        return redirect(('/profile/{}').format(new_name))
    return render_template('edit.html', form=form, user_name=user_name)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')