from sqlalchemy import (Column, Integer, String, DateTime,
                        Boolean, Numeric, Date, ForeignKey)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+pymysql://master:yusisheng123'
                       '@offer.cspfrhhjhhea.us-east-1.rds.amazonaws.com/'
                       'offer_2?charset=utf8mb4', pool_size=5, max_overflow=10,
                       pool_timeout=30, pool_recycle=3600)

Base = declarative_base()


class All_url(Base):
    __tablename__ = 'url'

    url_id = Column(Integer(), primary_key=True, autoincrement=False)
    url = Column(String(1000), index=True, unique=True)
    added_datetime = Column(DateTime(), default=datetime.now)
    source_site = Column(String(30))
    source_id = Column(Integer())
    scraped = Column(Boolean(), default=False)


class Applicant(Base):
    __tablename__ = "applicant"
    applicant_id = Column(Integer(), primary_key=True, autoincrement=False)
    name = Column(String(100), index=True, unique=True)
    toefl = Column(Integer())
    gre = Column(Integer())
    gre_aw = Column(Numeric(2, 1))
    college_name = Column(String(100))
    college_type = Column(String(10))
    gpa = Column(Numeric(5, 2))
    result_count = Column(Integer())
    updated_time = Column(DateTime(), default=datetime.now)
    link_id = Column(Integer(), ForeignKey('url.url_id'))


class Offer(Base):
    __tablename__ = "offer"

    offer_id = Column(Integer(), primary_key=True, autoincrement=False)
    applicant_id = Column(Integer(), ForeignKey('applicant.applicant_id'))
    univ_rank = Column(Integer())
    univ_name = Column(String(50))
    raw_univ_name = Column(String(50))
    app_time = Column(Date())
    result_time = Column(Date())
    result = Column(String(10))
    major = Column(String(30))
    raw_major = Column(String(30))
    degree = Column(String(10))
    url = Column(Integer(), ForeignKey('url.url_id'), nullable=False)
    comment = Column(String(1000), nullable=False)
    applicant = relationship("Applicant", backref=backref('offers',
                             order_by=result_time))


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
print(session.query(Offer).all())
session.close()
