import psycopg2
import getpass

class DataSource:
    def __init__(self):
        pass

    def connect(self, user, password):
        '''
		Establishes a connection to the database with the following credentials:
			user - username, which is also the name of the database
			password - the password for this database on perlman

		Note: exits if a connection cannot be established.
		'''
        try:
            self.connection = psycopg2.connect(host="localhost", database=user, user=user, password=password)
        except Exception as e:
            print("Connection error: ", e)
            exit()

    def disconnect(self):
        '''
        Breaks the connection to the database
        '''
        self.connection.close()

    def getHostInfo(self, host_id):
        '''
        Returns a list of all informations given the specified host id.
        Audience: hosts, tourists

        PARAMETERS:
            host_id - the unique id for each host

        RETURN:
            a list of all the informations of listings under the given host, or
            None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM airbnb where host_id = " + str(host_id)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getNumOfReviews(self, listing_id):
        '''
        Returns a list of a single element which is the number of reviews
        given the specified listing.
        Audience: hosts, tourists

        PARAMETERS:
            listing_id - the unique id for each listing

        RETURN:
            a list of a single element which is the number of reviews of that
            listing, or None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT number_of_reviews FROM airbnb where id = " + \
                    str(listing_id)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getPrice(self, listing_id):
        '''
        Returns a list of a single element which is the price of given specified
        listing.
        Audience: tourists, business owners, investigators/researchers,hosts

        PARAMETERS:
            listing_id - the unique id for each listing

        RETURN:
            a list of a single element which is the price of that listing, or
            None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT price FROM airbnb where id =" + str(listing_id)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getAvailability(self, listing_id):
        '''
        Returns a list of a single element which is the number of available
        days given specified listing.
        Audience: tourists, investigators/researchers

        PARAMETERS:
            listing_id - the unique id for each listing

        RETURN:
            a list of a single element which is the number of available days
            of the listing, or None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT availability_365 FROM airbnb where id =" + \
                    str(listing_id)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getSameHouseType(self, neighbourhood, room_type):
        '''
        Returns a list of listings given the neighbourhood area and listing
        space type.
        Audience: hosts, investigators/researchers

        PARAMETERS:
            neighbourhood - the neighbourhood area
            room_type - the listing space type

        RETURN:
            a list of listing_ids in the neighbourhood area of the specified
            room type, or None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT id FROM airbnb where neighbourhood = \'" + \
                    str(neighbourhood) + "\' and room_type = \'" + \
                    str(room_type) + "\'"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getPriceOfNeighbourhood(self, neighbourhood):
        '''
        Returns a list of prices given the neighbourhood area.
        Audience: hosts, tourists, business owners, investigators/researchers

        PARAMETERS:
            neighbourhood - the neighbourhood area

        RETURN:
            a list of prices of listings in the neighbourhood area, or None if
            the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT price FROM airbnb where neighbourhood = \'" + \
                    str(neighbourhood) + "\'"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getListingInfo(self, listing_id):
        '''
        Returns a list of a single tuple of informations of given listing id.
        Audience: tourists, hosts

        PARAMETERS:
            listing_id - the unique id for each listing

        RETURN:
            a list of a single tuple which contains all informations of given
            listing, or None if the query fails
        '''
        return []

    def getNumOfListings(self, neighbourhood_group, room_type):
        '''
        Returns a list of a single integer which is the number of listings given
        the neighbourhood borough and the room type.
        Audience: tourists, business owners, investigators/researchers

        PARAMETERS:
            neighbourhood_group - one of five boroughs of New York City
            room_type - the listing space type

        RETURN:
            a list of a single integer which is the number of listings given
            the neighbourhood borough and the room type, or None if the query
            fails
        '''
        return []

    def getSingleListingPercentage(self):
        '''
        Returns a float of percentage of hosts having only one listing
        Audience: investigators/researchers

        PARAMETERS:
            None

        RETURN:
            a float of percentage of hosts having only one listing, or None if
            the query fails
        '''
        return None

    def getAllListings(self, neighbourhood_group, room_type, price_range):
        '''
        Returns a list of tuples of listings' information given the
        neighbourhood borough and the room type and a tuple of price range
        Audience: tourists, investigators/researchers

        PARAMETERS:
            neighbourhood_group - one of five boroughs of New York City
            room_type - the listing space type
            price_range - minimum and maximum accepting price

        RETURN:
            a list of tuples of listings' information given the neighbourhood
            borough and the room type and the price range, or None if the query
            fails
        '''
        return []

    def getAverageAvailability(self, neighbourhood_group, room_type):
        '''
        Returns the average available nights for listings given the
        neighbourhood borough and room type.
        Audience: investigators/researchers

        PARAMETERS:
            neighbourhood_group - one of the five boroughs of New York City
            room_type - the listing space type

        RETURN:
            the average available nights of listings in the neighbourhood
            location of the specified room type, or None if the query fails
        '''
        return None

    def getAverageNumOfReviews(self, neighbourhood_group, room_type):
        '''
        Returns the average number of reviews for listings given the
        neighbourhood borough and room type.
        Audience: investigators/researchers

        PARAMETERS:
            neighbourhood_group - one of the five boroughs of New York City
            room_type - the listing space type

        RETURN:
            the average number of reviews of listings in the neighbourhood
            borough of the specified room type, or None if the query fails
        '''
        return None

    def getAveragePriceNbhGroup(self, neighbourhood_group, room_type):
        '''
        Returns the average price for listings given the neighbourhood borough
        and room type.
        Audience: investigators/researchers, business owners

        PARAMETERS:
            neighbourhood_group - one of the five boroughs of New York City
            room_type - the listing space type

        RETURN:
            the average price of listings in the neighbourhood
            borough of the specified room type, or None if the query fails
        '''
        return None

    def getAveragePriceNbh(self, neighbourhood, room_type):
        '''
        Returns the average price for listings given the neighbourhood area
        and room type.
        Audience: investigators/researchers, business owners

        PARAMETERS:
            neighbourhood_group - the neighbourhood area
            room_type - the listing space type

        RETURN:
            the average price of listings in the neighbourhood
            area of the specified room type, or None if the query fails
        '''
        return None

    def getAverage(self, list_of_nums):
        if not isinstance(list_of_nums, list):
            return "Input not list"
        for num in list_of_nums:
            if not isinstance(num, int):
                return "Invalid input"
        sum = 0
        count = 0
        for num in list_of_nums:
            sum += num
            count += 1
        return round(sum/count, 2)



def main():
    user = "qine"
    password = getpass.getpass()

    # Connect to the database
    query = DataSource()
    query.connect(user, password)

    # Query: host info
    host_info = query.getHostInfo(2787)

    if host_info is not None:
        print("Host info query results: ")
        for item in host_info:
            print(item)

    # Query: price
    price = query.getPrice(5295)

    if price is not None:
        print("Price query results: ")
        for item in price:
            print(item)

    # Query: availability
    availability = query.getAvailability(5295)

    if availability is not None:
        print("Availability info query results: ")
        for item in availability:
            print(item)

    # Disconnect from database
    query.disconnect()

main()
