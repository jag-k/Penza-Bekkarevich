from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from data import db_session, users
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from data.cart import Cart
from data.guitars import Guitars


db_session.global_init("db/shop.sqlite")


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            session.close()
            return redirect("/")
        session.close()
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        session.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    res = session.query(users.User).get(user_id)
    session.close()
    return res


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    return render_template("main.html")


@app.route("/catalog")
def catalog():
    session = db_session.create_session()
    catalogue = session.query(Guitars).all()
    num = 0
    if current_user.is_authenticated:
        for i in session.query(Cart).filter(Cart.user_id == current_user.id):
            num += int(i.quantity)
    session.close()
    return render_template("catalog.html", guitars=catalogue, num=num)


@app.route("/cart")
def cart():
    session = db_session.create_session()
    if not current_user.is_authenticated:
        return redirect("/register")
    basket = session.query(Cart).filter(Cart.user_id == current_user.id)
    if basket.first() is None:
        return render_template("empty_cart.html")
    total = 0
    for i in session.query(Cart).filter(Cart.user_id == current_user.id):
        total += int(i.cost[:-3].replace(' ', ''))
    return render_template("cart.html", cart=basket, total=total)


@app.route("/adding/<int:id>")
# @login_required
def adding(id):
    session = db_session.create_session()
    if not current_user.is_authenticated:
        return redirect("/register")
    guitar = session.query(Guitars).filter(Guitars.id == id).first()
    check = session.query(Cart).filter(Cart.product == id, Cart.user_id == current_user.id).first()
    if check is not None:
        check.quantity = int(check.quantity)
        check.quantity += 1
        check.cost = str(check.quantity * int(guitar.price[:-3].replace(' ', ''))) + ' р.'
        session.add(check)
        session.add(current_user)
        current_user.basket.append(check)
        session.merge(current_user)
        session.commit()
    else:
        b = Cart()
        session.add(b)
        session.add(current_user)
        if b.quantity is None:
            b.quantity = 0
        b.product = id
        b.quantity = int(b.quantity)
        b.quantity += 1
        b.cost = str(b.quantity * int(guitar.price[:-3].replace(' ', ''))) + ' р.'
        b.user_id = current_user.id
        current_user.basket.append(b)
        session.merge(current_user)
        session.commit()
    return redirect("/catalog")


@app.route("/delete/<int:id>")
def delete(id):
    session = db_session.create_session()
    rubbish = session.query(Cart).filter(Cart.id == id).first()
    if rubbish:
        if int(rubbish.quantity) > 1:
            rubbish.quantity = int(rubbish.quantity)
            price = int(rubbish.cost[:-3].replace(' ', '')) / rubbish.quantity
            rubbish.quantity -= 1
            rubbish.cost = str(rubbish.quantity * int(price)) + ' р.'
            session.add(rubbish)
            session.add(current_user)
            current_user.basket.append(rubbish)
            session.merge(current_user)
            session.commit()
        else:
            session.delete(rubbish)
            session.commit()
    else:
        abort(404)
    session.close()
    return redirect('/cart')


@app.route("/checkout")
def checkout():
    session = db_session.create_session()
    for i in session.query(Cart).filter(Cart.user_id == current_user.id):
        session.delete(i)
        session.commit()
    return render_template("checkout.html")


def main():
    db_session.global_init("db/shop.sqlite")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
