import json

__author__ = 'deathowl'
import time
from flask import Flask, render_template
from flask.ext.restful import reqparse, Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, distinct, select, UniqueConstraint
from sqlalchemy.exc import IntegrityError
import settings
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+settings.DB_PATH
except AttributeError:
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.ALCHEMY_URL

api = Api(app)
db = SQLAlchemy(app)

json_parser = reqparse.RequestParser()
json_parser.add_argument('hostname', type=unicode, required=True, location='json')
json_parser.add_argument('spec_result', type=unicode, required=True, location='json')
json_parser.add_argument('cookbook_name', type=unicode, required=True, location='json')

query_parser = reqparse.RequestParser()
query_parser.add_argument('hostname', type=unicode)
query_parser.add_argument('cookbook_name', type=unicode)
query_parser.add_argument('limit', type=int)

Base = declarative_base()
tests = Table('tests', Base.metadata,
              Column('id', db.Integer, primary_key=True),
              Column('hostname', db.String(100), index=True),
              Column('unix_timestamp', db.Integer, index=True),
              Column('spec_result', db.String(2000), index=True),
              Column('cookbook_name', db.String(100), index=True),
       )

Base.metadata.create_all(db.engine)


class Test(db.Model):
    __table__ = tests
    __mapper_args__ = {
        'primary_key': [tests.c.id]
    }

    def __init__(self, hostname, spec_result, cookbook_name):
        self.hostname = hostname
        self.unix_timestamp = int(time.time())
        self.spec_result = spec_result
        self.cookbook_name = cookbook_name


class TestList(Resource):
    def get(self):
        db_query = db.session.query(Test)
        query = query_parser.parse_args()
        #hostname
        if query['hostname'] is not None and query['hostname'] != '':
            db_query = db_query.filter(Test.hostname == query['hostname'])

        #cookbook_name
        if query['cookbook_name'] is not None and query['cookbook_name'] != '':
            db_query = db_query.filter(Test.cookbook_name == query['cookbook_name'])
        #limit
        if query['limit'] is not None:
            limit = int(query['limit'])
        else:
            limit = 20
        result = db_query.order_by(Test.unix_timestamp.desc()).limit(limit).all()
        mapped = [
            {"id": r.id,
             "hostname": r.hostname,
             "cookbook_name": r.cookbook_name,
             "timestamp": r.unix_timestamp,
             "status": "passed" if json.loads(r.spec_result)["summary"]["failure_count"] == 0 else "failed"
            } for r in result]

        return mapped

    def post(self):
        json = json_parser.parse_args()
        try:
            test = Test(json['hostname'], json['spec_result'], json['cookbook_name'])
            db.session.add(test)
            db.session.commit()

        except IntegrityError:
            pass  # This happens if we try to add the same test result multiple times
                 # Ignore it as we should
        return 'OK', 201

class TestResource(Resource):
    def get(self, reportid):
        test = db.session.query(Test).filter(Test.id == reportid).first()
        if test is not None:
            return json.loads(test.spec_result)#data already stored in json, do not escape it pls
        else:
            return "Not found", 404

api.add_resource(TestList, '/api/reports')
api.add_resource(TestResource, '/api/report/<reportid>')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host=settings.LISTEN_HOST, port=settings.LISTEN_PORT)