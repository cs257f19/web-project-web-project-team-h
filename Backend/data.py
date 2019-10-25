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
        '''
        Returns a list of a single element which is the number of available
        days given specified listing.

        PARAMETERS:
            connection - the connection to the database
            listing_id - the unique id for each listing

        RETURN:
            a list of a single element which is the number of available days
            of the listing, or None if the query fails
        '''
        try:
            cursor = connection.cursor()
            query = "SELECT availability_365 FROM airbnb where id =" + str(listing_id)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None


    def getSameHouseType(self, connection, neighbourhood, room_type):
        '''
        Returns a list of listings given the neighbourhood area and listing
        space type.

        PARAMETERS:
            connection - the connection to the database
            neighbourhood - the neighbourhood area
            room_type - the listing space type

        RETURN:
            a list of listing_ids in the neighbourhood area of the specified
            room type, or None if the query fails
        '''
        try:
            cursor = connection.cursor()
            query = "SELECT id FROM airbnb where neighbourhood = \'"+ str(neighbourhood) + "\' and room_type = \'" + str(room_type) + "\'"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getPriceOfNeighbourhood(self, connection, neighbourhood):
        '''
        Returns a list of prices given the neighbourhood area.

        PARAMETERS:
            connection - the connection to the database
            neighbourhood - the neighbourhood area

        RETURN:
            a list of prices of listings in the neighbourhood area, or None if
            the query fails
        '''
        try:
            cursor = connection.cursor()
            query = "SELECT price FROM airbnb where neighbourhood = \'" + str(neighbourhood) + "\'"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None
