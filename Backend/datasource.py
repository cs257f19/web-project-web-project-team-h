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
            a list of Listing objects of listings under the given host, or
            None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM airbnb where host_id = " + str(host_id)
            cursor.execute(query)
            listing_tuples = cursor.fetchall()
            listings = [Listing(a_tuple) for a_tuple in listing_tuples]
            return listings
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
            a list of a single Listing object which contains all informations
            of given listing, or None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM airbnb where listing_id = " + str(listing_id)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None


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
        try:
            cursor = self.connection.cursor()
            query = "SELECT count(list_id) FROM airbnb where neighbourhood = \'" + \
                    str(neighbourhood) + "\' and room_type = \'" + \
                    str(room_type) + "\'"

            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None


    def getHostSingleListingPct(self):
        '''
        Returns a float of percentage of hosts having only one listing
        Audience: investigators/researchers

        PARAMETERS:
            None

        RETURN:
            a float of percentage of hosts having only one listing, or None if
            the query fails
        '''

        try:
            cursor = self.connection.cursor()
            query = "SELECT "
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
        '''
        Returns the average value of a given list of numbers.

        PARAMETERS:
            list_of_nums - a list of numbers

        RETURN:
            the average value of numbers in the given list
        '''
        if not isinstance(list_of_nums, list):
            return "Input not list"
        if len(list_of_nums) == 0:
            return "Empty list"
        sum = 0
        count = 0
        for num in list_of_nums:
            if not isinstance(num, int):
                return "Invalid input"
            sum += num
            count += 1
        return round(sum/count, 2)


class Listing:
    '''
    This is the class for listing which stores all the information of a listings
    '''
    def __init__(self, listing_tuple):
        '''
        Constructor of the class

        PARAMETERS:
            listing_tuple - a tuple includes all the information of the listing,
                            returned by database query

        RETURN:
            None
        '''

        self.listing_id = listing_tuple[0]
        self.listing_name = listing_tuple[1]
        self.host_id = listing_tuple[2]
        self.host_name = listing_tuple[3]
        self.neighbourhood_group = listing_tuple[4]
        self.neighbourhood = listing_tuple[5]
        self.latitude = listing_tuple[6]
        self.longitude = listing_tuple[7]
        self.room_type = listing_tuple[8]
        self.price = listing_tuple[9]
        self.minimum_nights = listing_tuple[10]
        self.num_reviews = listing_tuple[11]
        self.reviews_per_month = listing_tuple[12]
        self.host_listings_count = listing_tuple[13]
        self.availability = listing_tuple[14]

    def getListingId(self):
        '''
        Returns the specific id for the given listing.

        PARAMETERS:
            None

        RETURN:
            the specific id for the given listing
        '''
        return self.listing_id

    def getListingName(self):
        '''
        Returns the specific description for the given listing.

        PARAMETERS:
            None

        RETURN:
            the specific description for the given listing
        '''
        return self.listing_name

    def getHostId(self):
        '''
        Returns the specific host id for the given listing.

        PARAMETERS:
            None

        RETURN:
            the specific host id for the given listing
        '''
        return self.host_id

    def getHostName(self):
        '''
        Returns the host name for the giving listing.

        PARAMETERS:
            None

        RETURN:
            the host name for the given listing
        '''
        return self.host_name

    def getNbhGroup(self):
        '''
        Returns the neighbourhood borough for the given listing.

        PARAMETERS:
            None

        RETURN:
            the neighbourhood borough for the given listing.
        '''
        return self.neighbourhood_group

    def getNbh(self):
        '''
        Returns the neighbourhood area for the given listing.

        PARAMETERS:
            None

        RETURN:
            the neighbourhood area for the given listing.
        '''
        return self.neighbourhood

    def getLatitude(self):
        '''
        Returns the latitude for the given listing.

        PARAMETERS:
            None

        RETURN:
            the latitude for the given listing.
        '''
        return self.latitude

    def getLongitude(self):
        '''
        Returns the longitude for the given listing.

        PARAMETERS:
            None

        RETURN:
            the longitude for the given listing.
        '''
        return self.longitude

    def getRoomType(self):
        '''
        Returns the room type for the given listing.

        PARAMETERS:
            None

        RETURN:
            the room type for the given listing.
        '''
        return self.room_type

    def getPrice(self):
        '''
        Returns the price for the given listing.

        PARAMETERS:
            None

        RETURN:
            the price for the given listing.
        '''
        return self.price

    def getNumReviews(self):
        '''
        Returns the number of reviews for the given listing.

        PARAMETERS:
            None

        RETURN:
            the number of reviews for the given listing.
        '''
        return self.num_reviews

    def getMinNights(self):
        '''
        Returns the minimum nights required to stay for the given listing.

        PARAMETERS:
            None

        RETURN:
            the minimum nights required to stay for the given listing.
        '''
        return self.minimum_nights

    def getReviewsPerMonth(self):
        '''
        Returns the number of reviews per month for the given listing.

        PARAMETERS:
            None

        RETURN:
            the number of reviews per month for the given listing.
        '''
        return self.reviews_per_month

    def getHostListingCount(self):
        '''
        Returns the number of listings under the same host for the given listing.

        PARAMETERS:
            None

        RETURN:
            the number of listings under the same host for the given listing.
        '''
        return self.host_listings_count

    def getNumAvailableDays(self):
        '''
        Returns the number of available days for the given listing.

        PARAMETERS:
            None

        RETURN:
            the number of available days for the given listing.
        '''
        return self.availability


def main():
    user = "qine"
    password = getpass.getpass()

    # Connect to the database
    query = DataSource()
    query.connect(user, password)

    # Query: host info
    host_info = query.getHostInfo(2787)

    if host_info is not None:
        print("Host info query results (only showing price here): ")
        for item in host_info:
            print(item.getPrice())

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
