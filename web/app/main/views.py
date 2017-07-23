from . import main
from flask import render_template, session, jsonify, redirect, url_for,\
                  flash, request
from flask_login import current_user
from .. import db
from ..model import All_url, Applicant, Offer, Visitor
from ..helper import (get_sum_offer, get_sum_applicant, get_applicant,
                      get_app_offer_count_from_dict, form_table_data,
                      Pagination, convert_string_to_bool, get_all_univ_name)
from sqlalchemy.sql.expression import and_
from sqlalchemy import desc, asc
from sqlalchemy.sql.expression import nullslast
from .form import Filter
from .major_list import major_list
from wtforms import BooleanField


RESULT_COUNT = 10


column_list = ["RESULT", "MAJOR",  "UNIVERSITY", "RANK", "RESULT TIME",
               "DEGREE", "COLLGE TYPE", "GPA", "GRE", "GRE AW", "TOEFL",
               "RESULTS", "SOURCE", "USER ID"]


@main.route("/")
def index():

    total_offer = get_sum_offer(db)
    total_applicant = get_sum_applicant(db)
    total_offer = "{:,}".format(total_offer)

    return render_template("index.html", total_offer=total_offer,
                           total_applicant=total_applicant)


@main.route("/user_basic/<int:user_id>")
def user_basic_into(user_id):
    pass


@main.route("/offer/<int:offer_id>")
def offer(offer_id):
    pass


@main.route("/applicant/<person_id>")
def applicant(person_id):

    result = db.session.query(Applicant.toefl.label("TOEFL"),
                              Applicant.gre.label("GRE"),
                              Applicant.gpa.label("GPA"),
                              Applicant.gpa.label("applicant_id"),
                              Applicant.gre_aw.label("GRE AW"),
                              Applicant.college_type.label("COLLGE TYPE"),
                              Applicant.source.label("SOURCE"),
                              Offer.univ_rank.label("RANK"),
                              Offer.univ_name.label("UNIVERSITY"),
                              Offer.result_time.label("RESULT TIME"),
                              Offer.major.label("MAJOR"),
                              Offer.degree.label("DEGREE"),
                              Offer.result.label("RESULT"),
                              Offer.url.label("URL"),
                              Applicant.person_id.label("USER ID"),
                              Offer.comment.label("COMMENT")).\
                              filter(and_(Offer.person_id == person_id,
                              Offer.applicant_id == Applicant.applicant_id,
                              Offer.univ_rank != None)).all()
    data = []
    data = form_table_data(db, result)
    title = data[0].get("USER ID")

    return render_template("search_by_rank.html", data=data, form=None,
                           column_list=column_list, pagination=None,
                           title=title)


@main.route("/search-by-name", methods=['GET', 'POST'])
def serach_by_name():
    args = request.args.copy()
    univ_list = args.get("univ_list", "1,2,3")

    if univ_list:
        univ_list = univ_list.split(",")

    class F(Filter):
        pass
    setattr(F, "min_rank", None)
    setattr(F, "max_rank", None)

    univ_rank_list = get_all_univ_name(db)

    for rank, name in univ_rank_list:
        default_value = False
        if str(rank) in univ_list:
            default_value = True
        setattr(F, str(rank) + "-" + str(name), BooleanField(str(rank) + "-" +
                str(name), id=rank,
                default=default_value))

    filter_toefl = (args.get("filter_toefl", False))
    filter_toefl = convert_string_to_bool(filter_toefl)
    filter_gpa = (args.get("filter_gpa", False))
    filter_gpa = convert_string_to_bool(filter_gpa)
    form = F(result=args.get("result", "All"),
                  degree=args.get("degree", ""),
                  filter_gpa=filter_gpa,
                  min_gpa=args.get("min_gpa", "2.0"),
                  max_gpa=args.get("max_gpa", "100"),
                  filter_toefl=filter_toefl,
                  min_toefl=args.get("min_toefl", "60"),
                  max_toefl=args.get("max_toefl", "120"),
                  major=args.get("major", ""),
                  sort=args.get("sort", "received_date"),
                  college_type=args.get("college_type", "")
                  )

    form.major.choices = major_list

    if form.validate_on_submit():
        args = request.args.copy()
        args["result"] = form.result.data
        args["degree"] = form.degree.data
        args["filter_gpa"] = form.filter_gpa.data
        args["min_gpa"] = form.min_gpa.data
        args["max_gpa"] = form.max_gpa.data
        args["filter_toefl"] = form.filter_toefl.data
        args["min_toefl"] = form.min_toefl.data
        args["max_toefl"] = form.max_toefl.data
        args["major"] = form.major.data
        args["sort"] = form.sort.data
        args["max_toefl"] = form.max_toefl.data
        args["college_type"] = form.college_type.data
        args["page"] = 1
        univ_list = []


        for item in dir(form):
            if item[0].isdigit():
                if form.__getattribute__(item).data:
                    rank_chosen = item.split("-")[0]
                    univ_list.append(str(rank_chosen))

        args["univ_list"] = ",".join(univ_list)

        return redirect(url_for(request.endpoint, **args))

    page = int(args.get('page', 1))
    offset = (int(page)-1)*RESULT_COUNT

    filter_toefl = (args.get("filter_toefl", False))
    filter_toefl = convert_string_to_bool(filter_toefl)
    filter_gpa = (args.get("filter_gpa", False))
    filter_gpa = convert_string_to_bool(filter_gpa)

    max_gpa = float(args.get('max_gpa', 100))
    min_gpa = float(args.get('min_gpa', 2))

    major = args.get('major', "")
    #  max_gre = int(args.get('max_gre', 340))
    #  min_gre = int(args.get('min_gre', 290))
    max_toefl = int(args.get('max_toefl', 60))
    min_toefl = int(args.get('min_toefl', 120))
    degree = args.get('degree', "")
    offer_result = args.get('result', "")
    college_type = args.get('college_type', "")
    sort = args.get('sort', "result_time")
    query = db.session.query(Applicant.toefl.label("TOEFL"),
                             Applicant.gre.label("GRE"),
                             Applicant.gpa.label("GPA"),
                             Applicant.gpa.label("applicant_id"),
                             Applicant.gre_aw.label("GRE AW"),
                             Applicant.college_type.label("COLLGE TYPE"),
                             Applicant.source.label("SOURCE"),
                             Offer.univ_rank.label("RANK"),
                             Offer.univ_name.label("UNIVERSITY"),
                             Offer.result_time.label("RESULT TIME"),
                             Offer.major.label("MAJOR"),
                             Offer.degree.label("DEGREE"),
                             Offer.result.label("RESULT"),
                             Offer.url.label("URL"),
                             Applicant.person_id.label("USER ID"),
                             Offer.comment.label("COMMENT")).filter(
                             and_(
                                  Applicant.applicant_id == Offer.applicant_id,
                                  Offer.univ_rank.in_(univ_list),
                                  Applicant.college_type.contains(college_type),
                                  Offer.degree.contains(degree),
                                  Offer.major.contains(major),
                                  Offer.result.contains(offer_result)
                                   )
                                )
    if filter_gpa:
        query = query.filter(Applicant.gpa.between(min_gpa, max_gpa))
    if filter_toefl:
        query = query.filter(Applicant.toefl.between(min_toefl, max_toefl))
    total_result = query.count()

    if sort == "gpa":
        query = query.order_by("gpa is NUll, gpa")
    elif sort == "toefl":
        query = query.order_by("toefl is NUll, toefl")
    elif sort == "rank":
        query = query.order_by("univ_rank is NUll, univ_rank")
    else:
        query = query.order_by(desc("RESULT TIME"))

    result = query.offset(offset).limit(RESULT_COUNT).all()
    data = []
    data = form_table_data(db, result)
    pagination = Pagination(page, RESULT_COUNT, total_result)

    return render_template("search_by_rank_copy.html", data=data,
                           total=total_result, form=form,
                           column_list=column_list, pagination=pagination,
                           title="Search by University Name")


@main.route("/search-by-rank", methods=['GET', 'POST'])
def serach_by_rank():
    args = request.args.copy()
    filter_toefl = (args.get("filter_toefl", False))
    filter_toefl = convert_string_to_bool(filter_toefl)
    filter_gpa = (args.get("filter_gpa", False))
    filter_gpa = convert_string_to_bool(filter_gpa)
    form = Filter(result=args.get("result", "All"),
                  degree=args.get("degree", ""),
                  min_rank=args.get("min_rank", "1"),
                  max_rank=args.get("max_rank", "80"),
                  filter_gpa=filter_gpa,
                  min_gpa=args.get("min_gpa", "2.0"),
                  max_gpa=args.get("max_gpa", "100"),
                  filter_toefl=filter_toefl,
                  min_toefl=args.get("min_toefl", "60"),
                  max_toefl=args.get("max_toefl", "120"),
                  major=args.get("major", ""),
                  sort=args.get("sort", "received_date"),
                  college_type=args.get("college_type", "")
                  )

    form.major.choices = major_list
    ip = request.access_route[-1]
    v = Visitor(ip=ip)
    db.session.add(v)
    db.session.commit()

    if form.validate_on_submit():
        args = request.args.copy()
        args["result"] = form.result.data
        args["degree"] = form.degree.data
        args["min_rank"] = form.min_rank.data
        args["max_rank"] = form.max_rank.data
        args["filter_gpa"] = form.filter_gpa.data
        args["min_gpa"] = form.min_gpa.data
        args["max_gpa"] = form.max_gpa.data
        args["filter_toefl"] = form.filter_toefl.data
        args["min_toefl"] = form.min_toefl.data
        args["max_toefl"] = form.max_toefl.data
        args["major"] = form.major.data
        args["sort"] = form.sort.data
        args["max_toefl"] = form.max_toefl.data
        args["college_type"] = form.college_type.data
        args["page"] = 1

        return redirect(url_for(request.endpoint, **args))

    page = int(args.get('page', 1))
    offset = (int(page)-1)*RESULT_COUNT

    filter_toefl = (args.get("filter_toefl", False))
    filter_toefl = convert_string_to_bool(filter_toefl)
    filter_gpa = (args.get("filter_gpa", False))
    filter_gpa = convert_string_to_bool(filter_gpa)

    max_gpa = float(args.get('max_gpa', 100))
    min_gpa = float(args.get('min_gpa', 2))
    max_rank = int(args.get('max_rank', 80))
    min_rank = int(args.get('min_rank', 1))
    major = args.get('major', "")
    max_gre = int(args.get('max_gre', 340))
    min_gre = int(args.get('min_gre', 290))
    max_toefl = int(args.get('max_toefl', 60))
    min_toefl = int(args.get('min_toefl', 120))
    degree = args.get('degree', "")
    offer_result = args.get('result', "")
    college_type = args.get('college_type', "")
    sort = args.get('sort', "result_time")
    query = db.session.query(Applicant.toefl.label("TOEFL"),
                             Applicant.gre.label("GRE"),
                             Applicant.gpa.label("GPA"),
                             Applicant.gpa.label("applicant_id"),
                             Applicant.gre_aw.label("GRE AW"),
                             Applicant.college_type.label("COLLGE TYPE"),
                             Applicant.source.label("SOURCE"),
                             Offer.univ_rank.label("RANK"),
                             Offer.univ_name.label("UNIVERSITY"),
                             Offer.result_time.label("RESULT TIME"),
                             Offer.major.label("MAJOR"),
                             Offer.degree.label("DEGREE"),
                             Offer.result.label("RESULT"),
                             Offer.url.label("URL"),
                             Applicant.person_id.label("USER ID"),
                             Offer.comment.label("COMMENT")).filter(
                             and_(
                                  Applicant.applicant_id == Offer.applicant_id,
                                  Offer.univ_rank.between(min_rank, max_rank),
                                  Applicant.college_type.contains(college_type),
                                  Offer.degree.contains(degree),
                                  Offer.major.contains(major),
                                  Offer.result.contains(offer_result)
                                   )
                                )
    if filter_gpa:
        query = query.filter(Applicant.gpa.between(min_gpa, max_gpa))
    if filter_toefl:
        query = query.filter(Applicant.toefl.between(min_toefl, max_toefl))
    total_result = query.count()

    if sort == "gpa":
        query = query.order_by("gpa is NUll, gpa")
    elif sort == "toefl":
        query = query.order_by("toefl is NUll, toefl")
    elif sort == "rank":
        query = query.order_by("univ_rank is NUll, univ_rank")
    else:
        query = query.order_by(desc("RESULT TIME"))

    result = query.offset(offset).limit(RESULT_COUNT).all()
    data = []
    data = form_table_data(db, result)
    pagination = Pagination(page, RESULT_COUNT, total_result)


    return render_template("search_by_rank_copy.html", data=data,
                           total=total_result, form=form,
                           column_list=column_list, pagination=pagination,
                           title="Search by University Rank")
