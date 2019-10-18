from flask import Flask, request, make_response, Response, jsonify
from flask_cors import CORS, cross_origin

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, User, Stream

engine = create_engine('sqlite:///streams.db')
Base.metadata.bind = engine

app = Flask("__main__")
CORS(app)


def start():
    """ Start a new database session for each database operation"""
    return sessionmaker(bind=engine)()


@app.route("/")
@app.route("/streams/")
@app.route("/streams")
@cross_origin()
def streams():
    db_session = start()
    streams_ = db_session.query(Stream).all()
    streams_json = [s.serialize for s in streams_]
    db_session.close()
    return jsonify(streams_json)


@app.route("/streams/<int:id>/")
@app.route("/streams/<int:id>")
@cross_origin()
def get_stream(id):
    db_session = start()
    stream = db_session.query(Stream).filter(Stream.id == id).one()
    stream_json = stream.serialize
    db_session.close()
    return jsonify(stream_json)


@app.route("/streams", methods=['POST'])
@cross_origin()
def create_stream():
    db_session = start()
    title = request.get_json()['title']
    description = request.get_json()['description']
    userId = request.get_json().get('userId')
    userId = '0' if userId is None else userId

    stream = Stream(title=title, description=description, user_id=userId)
    db_session.add(stream)
    db_session.commit()
    response = stream.serialize

    db_session.close()
    return jsonify(response)


@app.route("/streams/<int:id>", methods=['PUT'])
@cross_origin()
def update_stream(id):
    db_session = start()
    stream = db_session.query(Stream).filter(Stream.id == id).one()

    title = request.get_json()['title']
    description = request.get_json()['description']

    stream.title = title
    stream.description = description

    db_session.commit()
    response = stream.serialize
    db_session.close()

    return jsonify(response)


@app.route("/streams/<int:id>", methods=['DELETE'])
@cross_origin()
def delete_stream(id):
    db_session = start()
    stream = db_session.query(Stream).filter(Stream.id == id).one()

    db_session.delete(stream)
    db_session.commit()
    db_session.close()

    return Response()


if "__main__" == __name__:
    app.debug = True
    app.run()
