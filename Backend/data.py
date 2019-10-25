import psycopg2
import getpass

class Data:
    def __init__(self, connection):
        '''
        Initialize Data object for query purpose and connect to database.
        '''
        try:
            self.cursor = connection.cursor()
        except Exception as e:
    		print ("Connection error: ", e)

    def getHostInfo(self, host_id):
        '''
        Returns a list of all informations given the specified host id.

        PARAMETERS:
            host_id - the unique id for each host

        RETURN:
            a list of all the informations of listings under the given host, or
            None if the query fails
        '''
        try:
            query = "SELECT * FROM airbnb where host_id = " + str(host_id)
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None

    def getNumOfReviews(self, listing_id):
        '''
        Returns a list of a single element which is the number of reviews
        given the specified listing.

        PARAMETERS:
            listing_id - the unique id for each listing

        RETURN:
            a list of a single element which is the number of reviews of that
            listing, or None if the query fails
        '''
        try:
            query = "SELECT number_of_reviews FROM airbnb where id = " + str(listing_id)
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None

    def getPrice(self, listing_id):
        '''
        Returns a list of a single element which is the price of given specified
        listing.

        PARAMETERS:
            listing_id - the unique id for each listing

        RETURN:
            a list of a single element which is the price of that listing, or
            None if the query fails
        '''
        try:
            query = "SELECT price FROM airbnb where id =" + str(listing_id)
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None

    def getAvailability(self, listing_id):
        '''
        Returns a list of a single element which is the number of available
        days given specified listing.

        PARAMETERS:
            listing_id - the unique id for each listing

        RETURN:
            a list of a single element which is the number of available days
            of the listing, or None if the query fails
        '''
        try:
            query = "SELECT availability_365 FROM airbnb where id =" + str(listing_id)
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None

    def getSameHouseType(self, neighbourhood, room_type):
        '''
        Returns a list of listings given the neighbourhood area and listing
        space type.

        PARAMETERS:
            neighbourhood - the neighbourhood area
            room_type - the listing space type

        RETURN:
            a list of listing_ids in the neighbourhood area of the specified
            room type, or None if the query fails
        '''
        try:
            query = "SELECT id FROM airbnb where neighbourhood = \'" + \
            str(neighbourhood) + "\' and room_type = \'" + str(room_type) + "\'"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getPriceOfNeighbourhood(self, neighbourhood):
        '''
        Returns a list of prices given the neighbourhood area.

        PARAMETERS:
            neighbourhood - the neighbourhood area

        RETURN:
            a list of prices of listings in the neighbourhood area, or None if
            the query fails
        '''
        try:
            query = "SELECT price FROM airbnb where neighbourhood = \'" + \
            str(neighbourhood) + "\'"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
    		print ("Something went wrong when executing the query: ", e)
    		return None

    def getAverageAvailability(self, neighbourhood_group, room_type):
        '''
        Returns the average availablility nights for listings given the
        neighbourhood borough and room type.

        PARAMETERS:
            neighbourhood_group - one of the five boroughs of NYC
            room_type - the listing space type

        RETURN:
            the average price of listings in the neighbourhood location of the
            specified room type, or None if the query fails
        '''
        pass

    def getAverageNumOfReviews(self, neighbourhood_group, room_type):
        '''
        Returns the average number of reviews for listings given the
        neighbourhood borough and room type.

        PARAMETERS:
            neighbourhood_group - one of the five boroughs of NYC
            room_type - the listing space type

        RETURN:
            the average number of reviews of listings in the neighbourhood
            borough of the specified room type, or None if the query fails
        '''
        pass

    def getAveragePriceNbhGroup(self, neighbourhood_group, room_type):
        '''
        Returns the average price for listings given the neighbourhood borough
        and room type.

        PARAMETERS:
            neighbourhood_group - one of the five boroughs of NYC
            room_type - the listing space type

        RETURN:
            the average price of listings in the neighbourhood
            borough of the specified room type, or None if the query fails
        '''
        pass

    def getAveragePriceNbh(self, neighbourhood, room_type):
        '''
        Returns the average price for listings given the neighbourhood area
        and room type.

        PARAMETERS:
            neighbourhood_group - the neighbourhood area
            room_type - the listing space type

        RETURN:
            the average price of listings in the neighbourhood
            area of the specified room type, or None if the query fails
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
    query = Data(connection)
    results = query.getHostInfo(2787)

    if results is not None:
		print("Query results: ")
		for item in results:
			print(item)

	# Disconnect from database
    connection.close()

main()
