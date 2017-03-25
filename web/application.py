
from flask import Flask, render_template, session
from flask import redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from page import Pagination
from wtforms import BooleanField
from tools import get_pic, get_tablelist, get_total, get_first_pic, get_major_univ, general_random_password, update_visitor, get_total_offer, get_result_count, get_under_count,id_table_list,clean_userID
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from model import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail, Message
from form import Filter, Login_form, Register_form, Send_email, Update_passowrd
import matplotlib as mpl
from get_db import get_db
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


db, cursor = get_db()
major_list, univ_rank_list = get_major_univ(db, cursor)
db.close()

application = Flask(__name__)
application.config['SECRET_KEY'] = 'hard to guess string'

application.config['MAIL_SERVER'] = 'smtp.googlemail.com'
application.config['MAIL_PORT'] = 587
application.config['MAIL_USE_TLS'] = True
application.config['MAIL_USERNAME'] = "graduateoffer.get@gmail.com"
application.config['MAIL_PASSWORD'] = "yusisheng123"


login_manager = LoginManager()
bootstrap = Bootstrap(application)
moment = Moment(application)
mail = Mail(application)
login_manager.init_app(application)
expiration = 3600


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


def url_for_other_page(page_number):
    args = request.view_args.copy()
    args['page_number'] = page_number
    return url_for(request.endpoint, **args)
application.jinja_env.globals['url_for_other_page'] = url_for_other_page


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@application.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@application.route('/unisearch', methods=['GET', 'POST'])
def unisearch():
    class F(Filter):
        pass
    setattr(F, "rank", None)
    setattr(F, "start", None)
    setattr(F, "stop", None)
    for name in univ_rank_list:
        setattr(F, name, BooleanField(name))
    form = F()
    form.major.choices = major_list
    chosen_rank = []
    chosen_name = []
    if form.validate_on_submit():
        for item in dir(form):
            if item[0].isdigit():
                if form.__getattribute__(item).data:
                    rank_chosen = item.split("-")[0]
                    chosen_rank.append(str(rank_chosen))
                    chosen_name.append(item)
        if len(chosen_rank) == 0:
            flash('Please select your dream school')
            return redirect(url_for("unisearch"))
        session["rank_list"] = ",".join(chosen_rank)
        session["name_list"] = ",".join(chosen_name)
        session['result'] = form.result.data
        session['degree'] = form.degree.data
        session['under_cater'] = form.under_cater.data
        session['major'] = form.major.data
        session['count_per_page'] = form.count_per_page.data
        session['sort'] = form.sort.data
        session['order'] = form.order.data
        return redirect(url_for("dream_result", page_number=1))

    return render_template('dream_search.html', form=form,
                           table=None, img_data=None)


@application.route('/search', methods=['GET', 'POST'])
def search():
    form = Filter()
    form.major.choices = major_list
    table_list = []
    datas = None

    if form.validate_on_submit():
        session['result'] = form.result.data
        session['degree'] = form.degree.data
        session['start'] = form.start.data
        session["stop"] = form.stop.data
        session['under_cater'] = form.under_cater.data
        session['major'] = form.major.data
        session['count_per_page'] = form.count_per_page.data
        session['sort'] = form.sort.data
        session['order'] = form.order.data
        return redirect(url_for("seach_result", page_number=1))

    return render_template('search.html', form=form,
                           table=table_list, img_data=datas)


@application.route('/search_result/<page_number>', methods=['GET', 'POST'])
def seach_result(page_number):
    print("1")
    db, cursor = get_db()
    if session.get("start"):
        form = Filter(result=session['result'],
                      degree=session['degree'],
                      under_cater=session['under_cater'],
                      major=session['major'],
                      count_per_page=session['count_per_page'],
                      sort=session['sort'],
                      start=session["start"],
                      stop=session["stop"],
                      order=session["order"])
    else:
        form = Filter()
    print("2")
    form.major.choices = major_list
    table_list = []
    result = session['result']
    degree = session['degree']
    under_cater = session['under_cater']
    major = session['major']
    count_per_page = session['count_per_page']
    sort = session['sort']
    start = session["start"]
    stop = session["stop"]
    order = session["order"]
    datas = None
    if form.validate_on_submit():
        session['result'] = form.result.data
        session['degree'] = form.degree.data
        session['start'] = form.start.data
        session["stop"] = form.stop.data
        session['under_cater'] = form.under_cater.data
        session['major'] = form.major.data
        session['count_per_page'] = form.count_per_page.data
        session['sort'] = form.sort.data
        session['order'] = form.order.data
        return redirect(url_for("seach_result", page_number=1))
    print("3")

    if int(page_number) == 1:
        total_result = get_total(cursor=cursor, result=result, degree=degree,
                                 start=start, stop=stop,
                                 under_cater=under_cater, major=major,
                                 count_per_page=count_per_page)
        session["total_result"] = total_result
    print("4")
    table_list = get_tablelist(cursor=cursor, result=result, degree=degree,
                               start=start, stop=stop, under_cater=under_cater,
                               major=major, count_per_page=count_per_page,
                               sort=sort, order=order, page_number=page_number)
    print("5")
    total_result = session["total_result"]
    c_pag = Pagination(int(page_number), int(count_per_page),
                       int(total_result))
    db.close()
    print("6")

    return render_template('rank_result.html', table=table_list, form=form,
                           pagination=c_pag, img_data=datas,
                           total=session["total_result"])


@application.route('/dream_result/<page_number>', methods=['GET', 'POST'])
def dream_result(page_number):
    db, cursor = get_db()

    class F(Filter):
        pass
    setattr(F, "rank", None)
    setattr(F, "start", None)
    setattr(F, "stop", None)
    for name in univ_rank_list:
        setattr(F, name, BooleanField(name))
    dic = {}
    dic["result"] = session['result']
    dic["degree"] = session['degree']
    dic["under_cater"] = session['under_cater']
    dic["major"] = session['major']
    dic["count_per_page"] = session['count_per_page']
    dic["sort"] = session['sort']
    dic["order"] = session['order']
    name_list = session['name_list'].split(",")
    for name in name_list:
        dic[name] = True

    form = F(**dic)
    form.major.choices = major_list
    if form.validate_on_submit():
        chosen_rank = []
        chosen_name = []
        for item in dir(form):
            if item[0].isdigit():
                if form.__getattribute__(item).data:
                    rank_chosen = item.split("-")[0]
                    chosen_rank.append(str(rank_chosen))
                    chosen_name.append(item)
        if len(chosen_rank) == 0:
            flash('Please select your dream school')
            db.close()
            return redirect(url_for("unisearch"))
        session["rank_list"] = ",".join(chosen_rank)
        session["name_list"] = ",".join(chosen_name)
        session['result'] = form.result.data
        session['degree'] = form.degree.data
        session['under_cater'] = form.under_cater.data
        session['major'] = form.major.data
        session['count_per_page'] = form.count_per_page.data
        session['sort'] = form.sort.data
        session['order'] = form.order.data
        db.close()
        return redirect(url_for("dream_result", page_number=1))

    table_list = []
    result = session['result']
    degree = session['degree']
    under_cater = session['under_cater']
    major = session['major']
    count_per_page = session['count_per_page']
    sort = session['sort']
    order = session['order']
    rank_list = session["rank_list"]

    if int(page_number) == 1:
        total_result = get_total(cursor=cursor, result=result, degree=degree,
                                 rank_list=rank_list, under_cater=under_cater,
                                 major=major, count_per_page=count_per_page)
        session["total_result"] = total_result
    table_list = get_tablelist(cursor=cursor, result=result, degree=degree,
                               rank_list=rank_list, under_cater=under_cater,
                               major=major, count_per_page=count_per_page,
                               sort=sort, order=order, page_number=page_number)
    total_result = session["total_result"]
    c_pag = Pagination(int(page_number), int(count_per_page),
                       int(total_result))

    db.close()

    return render_template('dream_result.html', table=table_list, form=form,
                           pagination=c_pag, img_data=None,
                           total=session["total_result"])


@application.route('/', methods=['GET', 'POST'])
def first_page():
    db, cursor = get_db()
    ip = request.access_route[-1]
    update_visitor(db, cursor, ip)
    total_offer = get_total_offer(db, cursor)
    result_name, result_count, result_label = get_result_count(db, cursor,
                                                               'result')

    degree_name, degree_count, degree_label = get_result_count(db, cursor,
                                                               'degree')

    school_name, school_count, under_label = get_under_count(db, cursor,
                                                             'under_school_type')
    db.close()

    datas = []
    datas.append(get_first_pic(result_name, result_count,
                 result_label, "Application Results"))
    datas.append(get_first_pic(degree_name, degree_count,
                 degree_label, "Application Degree"))
    datas.append(get_first_pic(school_name, school_count,
                 under_label, "Applicants"))

    return render_template('first.html', datas=datas, total=total_offer)


@application.route('/login', methods=['GET', 'POST'])
def log_in():
    log_form = Login_form()
    if log_form.validate_on_submit():
        email = log_form.email.data
        password = log_form.password.data
        db, cursor = get_db()
        sql = """select password, activated from user where email = %s"""
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        db.close()

        if result:
            sql_pass = result[0]
            activated = result[1]
            if check_password_hash(sql_pass, password):
                if activated:
                    user = User(email)
                    login_user(user, log_form.remember_me.data)
                    flash('You have logged in!')
                else:
                    flash("You haven't activated your email yet.")
                return redirect(url_for("first_page"))
            else:
                flash('Password or Email not correct')
                return redirect(url_for("log_in"))
        else:
            flash('Password or Email not correct')
            return redirect(url_for("log_in"))

    return render_template("log_in.html", form=log_form)


@application.route('/register', methods=['GET', 'POST'])
def register():
    db, cursor = get_db()
    form = Register_form()
    if form.validate_on_submit():
        email = form.email.data
        sql = """select count(*) from user where email = %s """
        cursor.execute(sql, (email,))
        result = int(cursor.fetchone()[0])
        if result:
            flash("Email has been registered!")
            return render_template("register.html", form=form)
        password = form.password.data
        password = generate_password_hash(password)

        s = Serializer(application.config['SECRET_KEY'], expiration)
        token = (s.dumps({'confirm': email})).decode("utf-8")
        sql = """INSERT INTO user (email, password) VALUES (%s, %s)"""
        cursor.execute(sql, (email, password,))

        msg = Message("Verify Your Email",
                      sender="graduateoffer.get@gmail.com",
                      recipients=[email])
        msg.html = render_template("verify_email.html", token=token)
        with application.app_context():
            mail.send(msg)
        flash("Register sucess! Please verify your email.")
        db.commit()
        db.close()
        return redirect(url_for("log_in"))

    db.close()

    return render_template("register.html", form=form)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('first_page'))


@application.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    db, cursor = get_db()
    form = Send_email()
    if form.validate_on_submit():
        email = form.email.data
        sql = """select count(*) from user where email = %s"""
        cursor.execute(sql, (email, ))
        count = cursor.fetchone()[0]

        if count:
            password = general_random_password()
            hased_pass = generate_password_hash(password)
            flash("Email with new password has been send to you!")
            sql = """update user set password = %s where email = %s"""
            cursor.execute(sql, (hased_pass, email))
            db.commit()

            msg = Message("Your new password",
                          sender="graduateoffer.get@gmail.com",
                          recipients=[email])
            msg.html = render_template("new_password.html", password=password)
            with application.app_context():
                mail.send(msg)
        else:
            flash("Email does not exist.")
    db.close()

    return render_template("forgot_password.html", form=form)


@application.route('/verify/<token>')
def verify_email(token):
    db, cursor = get_db()
    s = Serializer(application.config['SECRET_KEY'])
    data = s.loads(token)
    email = data.get("confirm")
    sql = """select count(*) from user where email = %s"""
    cursor.execute(sql, (email, ))
    result = int(cursor.fetchone()[0])
    if result:
        sql = """update user set activated =1 where email = %s"""
        cursor.execute(sql, (email, ))
        db.commit()
        flash("Your account has been activated.")
        db.close()
        return redirect(url_for("first_page"))
    else:
        db.close()
        return render_template("404.html")


@application.route('/applicant/<person_id>')
def applicant_offer(person_id):
    db, cursor = get_db()
    table = id_table_list(cursor, person_id)
    person_id = clean_userID(person_id)
    return render_template('id_result.html', person_id=person_id, table=table)


@application.route('/rank_pic')
def rank_pic():
    db, cursor = get_db()
    result = session['result']
    degree = session['degree']
    under_cater = session['under_cater']
    major = session['major']
    count_per_page = session['count_per_page']
    start = session["start"]
    stop = session["stop"]
    img_data = get_pic(cursor=cursor, result=result, degree=degree,
                       start=start, stop=stop, under_cater=under_cater,
                       major=major, count_per_page=count_per_page)
    db.close()
    return render_template('rank_pic.html', img_data=img_data)


@application.route('/univ_pic')
def univ_pic():
    db, cursor = get_db()
    result = session['result']
    degree = session['degree']
    under_cater = session['under_cater']
    major = session['major']
    count_per_page = session['count_per_page']
    rank_list = session["rank_list"]
    img_data = get_pic(cursor=cursor, result=result, degree=degree,
                       rank_list=rank_list, under_cater=under_cater,
                       major=major, count_per_page=count_per_page)
    db.close()
    return render_template('rank_pic.html', img_data=img_data)


@application.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = Update_passowrd()
    if form.validate_on_submit():
        user = current_user
        old = form.old_pass.data
        new = form.new_pass.data
        if user.update_passowrd(old, new):
            flash("Password has been changed sucessfully.")
            return redirect(url_for("first_page"))
        else:
            flash("Old password is not correct")
            return redirect(url_for("change_password"))

    return render_template("reset_password.html", form=form)


if __name__ == '__main__':
    application.run(host='0.0.0.0')
