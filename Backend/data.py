import psycopg2
import getpass

class Data:
    def __init__(self):
        pass

    def getHostInfo(self, connection, host_id):
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM airbnb where host_id = " + str(host_id)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None


    def getNumOfReviews(self, connection, listing_id):
        try:
            cursor = connection.cursor()
            query = "SELECT number_of_reviews FROM airbnb where id = " + str(listing_id)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None

    def getPrice(self, connection, listing_id):
        try:
            cursor = connection.cursor()
            query = "SELECT price FROM airbnb where id =" + str(listing_id)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None


    def getAvailability(self, connection, listing_id):
        try:
            cursor = connection.cursor()
            query = "SELECT availability_365 FROM airbnb where id =" + str(listing_id)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None


    def getSameHouseType(self, connection, neighbourhood, room_type):
        try:
            cursor = connection.cursor()
            query = "SELECT id FROM airbnb where neighbourhood = \'"+ str(neighbourhood) + "\' and room_type = \'" + str(room_type) + "\'"
            cursor.execute(query)
            #return list of listings
            return cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getPriceOfNeighbourhood(self, connection, neighbourhood):
        try:
            cursor = connection.cursor()
            query = "SELECT price FROM airbnb where neighbourhood = \'" + str(neighbourhood) + "\'"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None
