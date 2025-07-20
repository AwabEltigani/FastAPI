from sqlalchemy import create_engine #creates the specific connection to the database
from sqlalchemy.ext.declarative import declarative_base #creates a base class for your orm model
from sqlalchemy.orm import sessionmaker #allows us to write python functions and statements translates to SQL
from FastAPI90.config import settings




#while True:
    #try:
        #conn = psycopg2.connect(host = "localhost", database = "FastAPI" ,user = 'postgres',password = 'Arsenalforever10&',cursor_factory=RealDictCursor)
        #cursor = conn.cursor()
        #print("Database connection was sucessful")
        #cursor.execute('SET search_path TO public;')
        #break
    #except Exception as error:
        #print("Database connection Failed")
        #print(f"Error: {error}")
        #time.sleep(2)

#'postgresql://<username>:<password>@<ip-adress/hostname>/<database_name>
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}'

#creating an engine to connect to our server
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#just copying default documentation from FASTAPI
SessionLocal = sessionmaker(autocommit = False,autoflush = False,bind = engine)

#defines our baseclasses for all our models that we define in postgres will extend this model
Base = declarative_base()

def get_db():
    db = SessionLocal() #What is responsible for connecting with our database
    #when it gets called it connects to our database allows us to communicate with it
    #when we are done it closes the connection to our database avoiding any errors
    try:
        yield db
    finally:
        db.close()