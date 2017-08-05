from sqlalchemy import (Column, Integer, String, DateTime,
                        Boolean, Numeric, Date, ForeignKey, Text)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+pymysql://master:yusisheng123'
                       '@offer.cspfrhhjhhea.us-east-1.rds.amazonaws.com/'
                       'offer_2?charset=utf8', pool_size=5, max_overflow=5,
                       pool_timeout=30, pool_recycle=3600, echo=False)

Base = declarative_base()


class Post(Base):
    __tablename__ = 'post'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8',
                      'mysql_collate': 'utf8_general_ci'}
    post_id = Column(Integer(), primary_key=True, autoincrement=True)
    user_name = Column(String(100), default="Visitor")
    content = Column(Text, default="Visitor")
    post_time = Column(DateTime(), default=datetime.now)


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8',
                      'mysql_collate': 'utf8_general_ci'}
    comment_id = Column(Integer(), primary_key=True, autoincrement=True)
    post_id = Column(Integer(), ForeignKey('post.post_id'))
    user_name = Column(String(100), default="Visitor")
    content = Column(Text, default="Visitor")
    comment_time = Column(DateTime(), default=datetime.now)

class All_url(Base):
    __tablename__ = 'url'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8',
                      'mysql_collate': 'utf8_general_ci'}
    url_id = Column(Integer(), primary_key=True, autoincrement=True)
    url = Column(String(1000), index=True, unique=True)
    added_datetime = Column(DateTime(), default=datetime.now)
    source = Column(String(30))
    tid = Column(Integer())
    scraped = Column(Boolean(), default=False)


class Applicant(Base):
    __tablename__ = "applicant"
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8',
                      'mysql_collate': 'utf8_general_ci'}
    applicant_id = Column(Integer(), primary_key=True, autoincrement=True)
    toefl = Column(Integer())
    gre = Column(Integer())
    gre_aw = Column(Numeric(2, 1))
    college_type = Column(String(10))
    gpa = Column(Numeric(5, 2))
    comment = Column(String(1000), nullable=True)
    person_id = Column(String(100))
    source = Column(String(10))
    version = Column(Integer(), default=1)
    updated_time = Column(DateTime(), default=datetime.now)

    def offer_cout(self, session):
        return session.query(Offer).filter(Offer.applicant_id ==
                                           self.applicant_id).count()


class Offer(Base):
    __tablename__ = "offer"
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8',
                      'mysql_collate': 'utf8_general_ci'}

    offer_id = Column(Integer(), primary_key=True, autoincrement=True)
    applicant_id = Column(Integer(), ForeignKey('applicant.applicant_id'))
    univ_rank = Column(Integer())
    univ_name = Column(String(50))
    raw_univ_name = Column(String(50))
    result_time = Column(Date())
    result = Column(String(10))
    major = Column(String(30))
    raw_major = Column(String(30))
    degree = Column(String(10))
    url = Column(String(1000))
    comment = Column(String(1000), nullable=True)
    source = Column(String(10))
    person_id = Column(String(100))

    applicant = relationship("Applicant", backref=backref('offers',
                             order_by=result_time))


def update_version(session, applicant):
    if applicant.person_id == "Anonymous":
        return None
    app = session.query(Applicant).\
        filter((Applicant.person_id == applicant.person_id) &
               (Applicant.source == applicant.source))
    print(app.count())
    if app.count() == 0:
        return None
    else:
        old_app = app.first()
        if not old_app.toefl:
            old_app.toefl = applicant.toefl
        if not old_app.gre:
            old_app.gre = applicant.gre
        if not old_app.gre_aw:
            old_app.gre_aw = applicant.gre_aw
        if not old_app.college_type == "211":
            old_app.college_type = applicant.college_type
        if not old_app.gpa:
            old_app.gpa = applicant.gpa
        session.commit()

        return app.one().applicant_id



class Visitor(Base):
    __tablename__ = "visitor"
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8',
                      'mysql_collate': 'utf8_general_ci'}
    applicant_id = Column(Integer(), primary_key=True, autoincrement=True)
    ip = Column(String(100))
    visit_time = Column(DateTime(), default=datetime.now)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


if __name__ == "__main__":
    applicant = Applicant(gpa=1, toefl=2, gre=3, gre_aw=4,
                          college_type="985", comment="hello",
                          person_id="nicole6927", source="point")

    print(update_version(session, applicant))
