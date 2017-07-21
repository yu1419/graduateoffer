from . import main
from flask import render_template, session, jsonify, redirect, url_for,\
                  flash, request
from flask_login import current_user
from .. import db
from ..model import All_url, Applicant, Offer
from ..helper import get_sum_offer, get_sum_applicant, get_applicant
from sqlalchemy.sql.expression import and_
RESULT_COUNT = 20


column_list = ["RESULT", "MAJOR",  "UNIVERSITY", "RANK", "RESULT TIME",
               "DEGREE", "COLLGE TYPE", "GPA", "GRE", "GRE AW", "TOEFL",
               "SOURCE", "PERSON ID", "COMMENT"]


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


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
def applicant(applicant_id):
    applicant_obj = get_applicant(db, person_id)
    offers = applicant_obj.offers
    print(len(offers))
    if applicant_obj:
        return render_template("index.html", applicant_obj=applicant_obj)


@main.route("/serach_by_name")
def serach_by_name():
    page = request.args.get('page', 1)
    offset = (int(page)-1)*RESULT_COUNT
    max_gpa = request.args.get('max_gpa', 100)
    min_gpa = request.args.get('min_gpa', 2)
    max_rank = request.args.get('max_rank', 80)
    min_rank = request.args.get('min_rank', 1)
    major = request.args.get('major', "")
    max_gre = request.args.get('max_gre', 340)
    min_gre = request.args.get('min_gre', 290)
    max_gre_aw = request.args.get('max_gre_aw', 6)
    min_gre_aw = request.args.get('min_gre_aw', 2)
    degree = request.args.get('degree', "")
    degree = "Master"
    offer_result = request.args.get('offer', "")
    college_type = request.args.get('college_type', "")
    order_by = request.args.get('offer', "order_by")
    result = db.session.query(Applicant.toefl.label("TOEFL"),
                              Applicant.gre.label("GRE"),
                              Applicant.gpa.label("GPA"),
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
                              Applicant.person_id.label("PERSON ID"),
                              Offer.comment.label("COMMENT")).filter(
                              and_(Applicant.gpa.between(min_gpa, max_gpa),
                                   Applicant.applicant_id == Offer.applicant_id,
                                   Applicant.gpa.between(min_gpa, max_gpa),
                                   Applicant.gre.between(min_gre, max_gre),
                                   Applicant.gre_aw.between(min_gre_aw,
                                                            max_gre_aw),
                                   Offer.univ_rank.between(min_rank, max_rank),
                                   Applicant.college_type.contains(college_type),
                                   Offer.degree.contains(degree),
                                   Offer.major.contains(major),
                                   Offer.result.contains(offer_result)
                                   )
                                ).offset(offset).limit(RESULT_COUNT).all()

    data=[]
    for x in result:
        data.append(x._asdict())

    return render_template("serach_by_name.html", data=data,
                           column_list=column_list)


@main.route("/serach_by_rank")
def serach_by_rank():
    return render_template("index.html")
