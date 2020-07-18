from flask import Flask, request, jsonify
import os, psycopg2, uuid
from dotenv import load_dotenv
load_dotenv("./.env")

app = Flask(__name__)
@app.route("/post", methods=["POST"])
def respond():
    data = request.json
    callDB(data,request.remote_addr)
    if "key" in data and "numfiles" in data:
        return jsonify(data)
    else:
        return jsonify({"error":"No key or numfiles provided"})

def callDB(data,ip):
    try:
        connection = psycopg2.connect(user = os.getenv("DB_USER"),
                                    password = os.getenv("DB_PASSWORD"),
                                    host = os.getenv("DB_HOST"),
                                    port = os.getenv("DB_PORT"),
                                    database = os.getenv("DB_DB"))
        cursor = connection.cursor()

        # QUERY
        query = ("INSERT INTO \"data\" (unique_id,key,numfiles,ip) VALUES (%s,%s,%s,%s)")
        record = (str(uuid.uuid4()),data["key"],data["numfiles"],ip)
        print("inserting",record)
        cursor.execute(query,record)
        connection.commit()

        # record = cursor.fetchone()
        # print("You are connected to - ", record,"\n")
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                # Closing db connection






if __name__=="__main__":
    app.run(threaded=True, port=5000)
