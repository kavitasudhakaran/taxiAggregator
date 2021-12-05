
from src.Utils.database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId


# Taxi document contains reg no (String), brand (String), model (String), type (String) and currentLocation (GeoJSON)fields
class TaxiModel:
    TAXI_COLLECTION = 'taxis'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since taxi reg no should be unique in taxis collection, this provides a way to fetch the taxi document based on the taxi reg no
    def find_taxi_by_reg_no(self, reg_no):
        key = {'reg_no': reg_no}
        return self.__find(key)

    # Finds a document based on the unique auto-generated MongoDB object id
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)

    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        taxi_document = self._db.get_single_data(TaxiModel.TAXI_COLLECTION, key)
        return taxi_document

    # This first checks if a taxi already exists with that reg no. If it does, it populates latest_error and returns -1
    # If a taxi doesn't already exist, it'll insert a new document and return the same to the caller
    def insertNewTaxi(self, reg_no,model, brand, type, vacant, base_rate, lat,long):
        self._latest_error = ''
        print("Inserting data for New Taxi with reg_no - "+reg_no+" to Taxis Collection....")
        taxis_document = self.find_taxi_by_reg_no(reg_no)
        if (taxis_document):
            self._latest_error = f'Taxi with Regd No-  {reg_no} already exists'
            return -1
        currentCoordinates = {'type': "Point", 'coordinates': [lat, long]}
        taxi_data = {'reg_no': reg_no, 'brand': brand, 'model': model, 'type': type, 'base_rate': base_rate,
                     'vacant': vacant, 'currentCoordinates': currentCoordinates}

        taxi_obj_id = self._db.insert_single_data(TaxiModel.TAXI_COLLECTION, taxi_data)
        return self.find_by_object_id(taxi_obj_id)
