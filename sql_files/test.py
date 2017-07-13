from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://master:yusisheng123'
                       '@offer.cspfrhhjhhea.us-east-1.rds.amazonaws.com/'
                       'offer_2',
                       pool_recycle=3600)
connection = engine.connect()
