from flask import Flask, render_template, session, redirect
from forms import LoginForm, RegForm, EditForm, CreateForm, EditComForm
from models import DB, UserModel, NewsModel, CommunityModel


app = Flask(__name__)
app.config['SECRET_KEY'] = 'polina_secret_key'
db = DB()
user_model = UserModel(db.get_connection())
user_model.init_table()
news_model = NewsModel(db.get_connection())
news_model.init_table()
community_model = CommunityModel(db.get_connection())
community_model.init_table()

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
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
    form = RegForm()
    user_name = form.username.data
    password = form.password.data
    user_model = UserModel(db.get_connection())
    existence = ''
    if not user_name in [tuply[1] for tuply in user_model.get_all()] and not (user_name is None) and not (password is None):
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
    user = user_model.get_name(user_name)[0]
    news = NewsModel(db.get_connection()).get_all(user)
    comm = UserModel(db.get_connection()).get(user)[3].split()
    communities = [community_model.get(int(i))[1] for i in comm]
    return render_template('profile.html', user_name=user_name, news=news, communities=communities)

@app.route('/profile/<user_name>/edit', methods=['GET', 'POST'])
def edit(user_name):
    if 'username' not in session:
        return redirect('/login')
    form = EditForm()
    if session['username'] != user_name:
        return redirect(('/profile/{}').format(user_name))
    user_model = UserModel(db.get_connection())
    new_name = form.username.data
    existence = ''
    if not new_name in [tuply[1] for tuply in user_model.get_all()] and not new_name is None:
        user_model.update(new_name, session['user_id'])
        session['username'] = new_name
        return redirect(('/profile/{}').format(new_name))
    elif not new_name is None:
        existence = 'This name is taken'
    return render_template('edit.html', form=form, user_name=user_name, existence=existence)

@app.route('/community/<community_name>', methods=['GET'])
def community(community_name):
    if 'username' not in session:
        return redirect('/login')
    user_name = session['username']
    community = CommunityModel(db.get_connection()).get_name(community_name)
    news = NewsModel(db.get_connection()).get_all(None, community[0])
    admin = int(community[3].split()[0])
    users = [user_model.get(int(i))[1] for i in community[3].split()]
    bio = community[2]
    if session['username'] in users:
        followed = True
    else:
        followed = False
    print(followed)
    return render_template('community.html', community_name=community_name, bio=bio, user_name=user_name, news=news, users=users, admin=admin, followed=followed)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect('/login')
    form = CreateForm()
    community_name = form.title.data
    bio = form.bio.data
    existence = ''
    if not community_name in [tuply[1] for tuply in community_model.get_all()] and not (community_name is None) and not (bio is None):
        community_model.insert(community_name, bio, session['user_id'])
        user_model.follow(session['user_id'], community_model.get_name(community_name)[0])
        return redirect(('/community/{}').format(community_name))
    elif not (community_name is None) and not (bio is None):
        existence = 'This name is taken'
    return render_template('create.html', form=form, existence=existence)

@app.route('/follow/<community_name>')
def follow(community_name):
    user_id = session['user_id']
    com_id = community_model.get_name(community_name)[0]
    users = community_model.get_name(community_name)[3].split()
    if not user_id in users:
        user_model.follow(user_id, com_id)
        community_model.follow(user_id, com_id)
    return redirect(('/community/{}').format(community_name))

@app.route('/community/<community_name>/edit', methods=['GET', 'POST'])
def edit_com(community_name):
    if 'username' not in session:
        return redirect('/login')
    form = EditComForm()
    community = CommunityModel(db.get_connection()).get_name(community_name)
    admin = int(community[3].split()[0])
    if session['user_id'] != admin:
        return redirect(('/community/{}').format(community_name))
    title = form.title.data
    bio = form.bio.data
    existence = ''
    if not title in [tuply[1] for tuply in community_model.get_all()] and (not title is None or not bio is None):
        community_model.update(community[0], title, bio)
        if title is '':
            title = community_name
        return redirect(('/community/{}').format(title))
    elif not title is None:
        existence = 'This name is taken'
    return render_template('editcom.html', form=form, existence=existence)

@app.route('/unfollow/<community_name>')
def unfollow(community_name):
    user_id = session['user_id']
    com_id = community_model.get_name(community_name)[0]
    users = community_model.get_name(community_name)[3].split()
    if str(user_id) in users:
        user_model.unfollow(user_id, com_id)
        community_model.unfollow(user_id, com_id)
    return redirect(('/community/{}').format(community_name))



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')