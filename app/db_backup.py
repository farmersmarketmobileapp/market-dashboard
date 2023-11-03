import os
from dotenv import  load_dotenv
import pymongo
import json
from datetime import datetime

if os.name == 'nt':
    load_dotenv()

# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


def get_database(name: str):
    conn_str = os.getenv('MONGODB_CONNECTION_STRING')
    print(conn_str)
    myclient = pymongo.MongoClient(conn_str)
    print(myclient)
    db = myclient.get_database(name) #database name
    return db, myclient


def save_collection_to_json(collection_name: str="_User", output_path="../data/user_test.json"):
    """

    :param db_name: name of mono db (can be found on sashido)
    :param collection_name: name of collection in mono db (_SCHEMA, Advert, _Installation, system.profile,
    _JobSchedule, _Log, _User, ReviewTotal, Reviews, _Role, _Session
    :param output_path: where to store the json output
    :return:
    """
    db, myclient = get_database(name=os.getenv("DB_NAME"))

    # list all collections
    #cursor = db.list_collection_names()
    #for c in cursor:
    #    print(c)

    # Select the collection from which you want to load data
    collection = db.get_collection(collection_name)
    # Query to retrieve data from the collection
    query = {}  # You can specify a query to filter the documents you want to export
    # Fetch data from the collection
    cursor = collection.find(query)
    # Convert the cursor to a list of dictionaries
    data = list(cursor)
    # Define the path and name of the JSON file
    json_filename = output_path
    # Save the data to a JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4, cls=DateTimeEncoder)
    myclient.close()


def run_db_backup(date: str = "2023_11_02"):
    save_collection_to_json(collection_name="_User", output_path=f"../data/user_save_{date}.json")
    save_collection_to_json(collection_name="Advert", output_path=f"../data/advert_save_{date}.json")
    save_collection_to_json(collection_name="Reviews", output_path=f"../data/reviews_save_{date}.json")
    save_collection_to_json(collection_name="ReviewTotal", output_path=f"../data/reviewsTotal_save_{date}.json")
    save_collection_to_json(collection_name="_Session", output_path=f"../data/session_save_{date}.json")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    run_db_backup()
