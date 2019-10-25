import psycopg2
import getpass

class Data:
    def __init__(self):
        pass

    def getHostInfo(self, connection, host_id):
        '''
        Returns a list of all informations given the specified host id.

        PARAMETERS:
            connection - the connection to the database
            host_id - the unique id for each host

        RETURN:
            a list of all the informations of listings under the given host, or
            None if the query fails
        '''
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM airbnb where host_id = " + str(host_id)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None

    def getNumOfReviews(self, connection, listing_id):
        '''
        Returns a list of a single element which is the number of reviews
        given the specified listing.

        PARAMETERS:
            connection - the connection to the database
            listing_id - the unique id for each listing

        RETURN:
            a list of a single element which is the number of reviews of that
            listing, or None if the query fails
        '''
        try:
            cursor = connection.cursor()
            query = "SELECT number_of_reviews FROM airbnb where id = " + str(listing_id)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None

    def getPrice(self, connection, listing_id):
        '''
        Returns a list of a single element which is the price of given specified
        listing.

        PARAMETERS:
            connection - the connection to the database
            listing_id - the unique id for each listing

        RETURN:
            a list of a single element which is the price of that listing, or
            None if the query fails
        '''
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

    def getAverageAvailability(self, connection, neighbourhood_group, room_type):
        '''
        Returns the average availablility nights for listings given the
        neighbourhood location and room type.

        PARAMETERS:
            connection - the connection to the database
            neighbourhood_group - the neighbourhood location
            room_type - the listing space type

        RETURN:
            the average price of listings in the neighbourhood location of the
            specified room type, or None if the query fails
        '''
        pass

    def getAverageNumOfReviews(self, connection, neighbourhood_group, room_type):
        '''
        Returns the average number of reviews for listings given the
        neighbourhood location and room type.

        PARAMETERS:
            connection - the connection to the database
            neighbourhood_group - the neighbourhood location
            room_type - the listing space type

        RETURN:
            the average number of reviews of listings in the neighbourhood
            location of the specified room type, or None if the query fails
        '''
        pass

    def getAveragePrice(self, connection, neighbourhood_group, room_type):
        '''
        Returns the average price for listings given the
        neighbourhood location and room type.

        PARAMETERS:
            connection - the connection to the database
            neighbourhood_group - the neighbourhood location
            room_type - the listing space type

        RETURN:
            the average price of listings in the neighbourhood
            location of the specified room type, or None if the query fails
        '''
        pass

def connect(user, password):
	'''
	Establishes a connection to the database with the following credentials:
		user - username, which is also the name of the database
		password - the password for this database on perlman

	Returns: a database connection.

	Note: exits if a connection cannot be established.
	'''
	try:
		connection = psycopg2.connect(database=user, user=user, password=password)
	except Exception as e:
		print("Connection error: ", e)
		exit()
	return connection


def main():

    user = "qine"
    password = getpass.getpass()

    # Connect to the database
    connection = connect(user, password)

	# Execute a simple query: how many earthquakes above the specified magnitude are there in the data?
    query = Data()
    results = query.getHostInfo(connection, 2787)

    if results is not None:
		print("Query results: ")
		for item in results:
			print(item)

	# Disconnect from database
    connection.close()

main()
