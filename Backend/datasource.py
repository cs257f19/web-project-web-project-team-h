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
            a list of Listing objects in the neighbourhood area of the specified
            room type, or None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM airbnb where neighbourhood = \'" + \
                    str(neighbourhood) + "\' and room_type = \'" + \
                    str(room_type) + "\'"
            cursor.execute(query)
            listing_tuples = cursor.fetchall()
            listings = [Listing(a_tuple) for a_tuple in listing_tuples]
            return listings
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
        Returns a list of all informations of a lising of the given listing id.
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
            listing_tuples = cursor.fetchall()
            assert len(listing_tuples)==1, \
                   'the listing id does not exist or is not unique'
            listings = [Listing(a_tuple) for a_tuple in listing_tuples]
            return listings
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

    def getNumHostNumListing(self):
        '''

        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT host_id FROM airbnb"
            cursor.execute(query)
            all_info = cursor.fetchall()
            host_listings_num = {}
            for host in all_info:
                host_id = host[0]
                if host_id not in host_listings_num:
                    host_listings_num[host_id] = 0
                host_listings_num[host_id] += 1

            listing_num = {}
            for host, num in host_listings_num.items():
                if num not in listing_num:
                    listing_num[num] = 0
                listing_num[num] += 1

            return listing_num
        except Exception as e:
            print("Something went wrong when getting the number of listing for hosts:", e)
            return None

    def getSingleMultipleListing(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(host_id) FROM airbnb"
            cursor.execute(query)
            total = cursor.fetchall()[0][0]
            listing_num = self.getNumHostNumListing()
            single_listing = listing_num[1]
            multiple_listing = total - single_listing
            return (single_listing, multiple_listing)
        except Exception as e:
            print("Something went wrong when executing get single and multiple listing:", e)
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
        single, multiple = self.getSingleMultipleListing()
        total = single + multiple
        percentage = float(single/total)
        return percentage

    def getAllListings(self, neighbourhood_group, room_type, price_range):
        '''
        Returns a list of Listing objects that contains listing info given the
        neighbourhood borough and the room type and a tuple of price range
        Audience: tourists, investigators/researchers

        PARAMETERS:
            neighbourhood_group - one of five boroughs of New York City
            room_type - the listing space type
            price_range - minimum and maximum accepting price

        RETURN:
            a list of Listing objects that contains listing info given the 
            neighbourhood borough and the room type and the price range, 
            or None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            min_price = price_range[0]
            max_price = price_range[1]
            print('min p', min_price)
            query = "SELECT * FROM airbnb where neighbourhood_group = \'" + \
                    str(neighbourhood_group) + "\' and room_type = \'" + \
                    str(room_type) + "\' and price > " + str(min_price) + \
                    " and price < " + str(max_price)
            print('query', query)
            cursor.execute(query)
            listing_tuples = cursor.fetchall()
            listings = [Listing(a_tuple) for a_tuple in listing_tuples]
            return listings
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None

    def getAverageAvailability(self, neighbourhood_group=None, room_type=None):
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
        try:
            cursor = self.connection.cursor()
            if neighbourhood_group is None and room_type is None:
                query = "SELECT AVG(availability_365) FROM airbnb"
            else:
                query = "SELECT AVG(availability_365) FROM airbnb where " + \
                        "neighbourhood_group = \'" + str(neighbourhood_group) + \
                        "\' and room_type = \'" + str(room_type) + "\'"
            cursor.execute(query)
            return float(cursor.fetchall()[0][0])
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None

    def getAverageNumOfReviews(self, neighbourhood_group=None, room_type=None):
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
        try:
            cursor = self.connection.cursor()
            if neighbourhood_group is None and room_type is None:
                query = "SELECT AVG(number_of_reviews) FROM airbnb"
            else:
                query = "SELECT AVG(number_of_reviews) FROM airbnb where " + \
                        "neighbourhood_group = \'" + str(neighbourhood_group) + \
                        "\' and room_type = \'" + str(room_type)+"\'"
            cursor.execute(query)
            return float(cursor.fetchall()[0][0])
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None

    def getAveragePriceNbhGroup(self, neighbourhood_group=None, room_type=None):
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
        try:
            cursor = self.connection.cursor()
            if neighbourhood_group is None and room_type is None:
                query = "SELECT AVG(price) FROM airbnb"
            else:
                query = "SELECT AVG(price) FROM airbnb where " + \
                        "neighbourhood_group = \'" + str(neighbourhood_group) + \
                        "\' and room_type = \'" + str(room_type) + "\'"
            cursor.execute(query)
            return float(cursor.fetchall()[0][0])
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None

    def getAveragePriceNbh(self, neighbourhood=None, room_type=None):
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
        try:
            cursor = self.connection.cursor()
            if neighbourhood is None and room_type is None:
                query = "SELECT AVG(price) FROM airbnb"
            else:
                query = "SELECT AVG(price) FROM airbnb where " + \
                        "neighbourhood = \'" + str(neighbourhood) + \
                        "\' and room_type = \'" + str(room_type) + "\'"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None

    def getCertainRoomTypeCount(self, room_type):
        '''
        Helper function for getRoomTypeForAll(self)
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(id) FROM airbnb where room_type = \'" + \
                    str(room_type) + "\'"
            cursor.execute(query)
            return cursor.fetchall()[0][0]
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None

    def getTotalReviews(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT SUM(number_of_reviews) FROM airbnb"
            cursor.execute(query)
            return cursor.fetchall()[0][0]
        except Exception as e:
            print("Something went wrong when executing the query:", e)
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
        Constructor of the class.

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
            the specific id for the given listing, or 0 if the listing id does
            not exist
        '''
        if self.listing_id is None:
            print("Listing not exists.")
            return 0
        return self.listing_id

    def getListingName(self):
        '''
        Returns the specific description for the given listing.

        PARAMETERS:
            None

        RETURN:
            the specific description for the given listing, or a string
            "Unavailable listing name" is the listing name does not exist
        '''
        if self.listing_name is None:
            print("Listing name is not available for this listing.")
            return "Unavailable listing name"
        self.listing_name = self.listing_name.replace('\n','')
        return self.listing_name

    def getHostId(self):
        '''
        Returns the specific host id for the given listing.

        PARAMETERS:
            None

        RETURN:
            the specific host id for the given listing, or 0 if the host id does
            not exist
        '''
        if self.host_id is None:
            print("Host not exists.")
            return 0
        return self.host_id

    def getHostName(self):
        '''
        Returns the host name for the giving listing.

        PARAMETERS:
            None

        RETURN:
            the host name for the given listing, or "Unavailable" if the host
            name does not exist
        '''
        if self.host_name is None:
            print("Host name not available for this listing.")
            return "Unavailable"
        return self.host_name

    def getNbhGroup(self):
        '''
        Returns the neighbourhood borough for the given listing.

        PARAMETERS:
            None

        RETURN:
            the neighbourhood borough for the given listing, or the neighbourhood
            group does not exist
        '''
        if self.neighbourhood_group is None:
            print("Neighbourhood borough for this listing is not available.")
            return "Unavailable"
        return self.neighbourhood_group

    def getNbh(self):
        '''
        Returns the neighbourhood area for the given listing.

        PARAMETERS:
            None

        RETURN:
            the neighbourhood area for the given listing, or the neighbourhood
            does not exist
        '''
        if self.neighbourhood is None:
            print("Neighbourhood for this listing is not available.")
            return "Unavailable"
        return self.neighbourhood

    def getLatitude(self):
        '''
        Returns the latitude for the given listing.

        PARAMETERS:
            None

        RETURN:
            the latitude for the given listing, or 0 if the latitude does not
            exist
        '''
        if self.latitude is None:
            print("Latitude for this listing not available.")
            return 0
        return self.latitude

    def getLongitude(self):
        '''
        Returns the longitude for the given listing.

        PARAMETERS:
            None

        RETURN:
            the longitude for the given listing, or 0 if the longitude does not
            exist
        '''
        if self.longitude is None:
            print("Longitude for this listing is not available.")
            return 0
        return self.longitude

    def getRoomType(self):
        '''
        Returns the room type for the given listing.

        PARAMETERS:
            None

        RETURN:
            the room type for the given listing, or "Unavailable" if the room
            type does not exist
        '''
        if self.room_type is None:
            print("Room type for this listing not available.")
            return "Unavailable"
        return self.room_type

    def getPrice(self):
        '''
        Returns the price for the given listing.

        PARAMETERS:
            None

        RETURN:
            the price for the given listing, or 0 if the price does not exist
        '''
        if self.price is None:
            print("Price for this listing not available.")
            return 0
        return self.price

    def getNumReviews(self):
        '''
        Returns the number of reviews for the given listing.

        PARAMETERS:
            None

        RETURN:
            the number of reviews for the given listing, or 0 if the number of
            reviews does not exist
        '''
        if self.num_reviews is None:
            print("Number of reviews for this listing not available.")
            return 0
        return self.num_reviews

    def getMinNights(self):
        '''
        Returns the minimum nights required to stay for the given listing.

        PARAMETERS:
            None

        RETURN:
            the minimum nights required to stay for the given listing, or 0 if
            the minimum number of nights does not exist
        '''
        if self.minimum_nights is None:
            print("Number of the minimum nights required for this listing not available.")
            return 0
        return self.minimum_nights

    def getReviewsPerMonth(self):
        '''
        Returns the number of reviews per month for the given listing.

        PARAMETERS:
            None

        RETURN:
            the number of reviews per month for the given listing, or 0 if the
            number of reviews per month does not exist
        '''
        if self.reviews_per_month is None:
            print("Number of reviews per month for this listing not available.")
            return 0
        return self.reviews_per_month

    def getHostListingCount(self):
        '''
        Returns the number of listings under the same host for the given listing.

        PARAMETERS:
            None

        RETURN:
            the number of listings under the same host for the given listing, or
            0 if the number of listings under the same host does not exist
        '''
        if self.host_listings_count is None:
            print("Number of listings under the same host not available.")
            return 0
        return self.host_listings_count

    def getNumAvailableDays(self):
        '''
        Returns the number of available days for the given listing.

        PARAMETERS:
            None

        RETURN:
            the number of available days for the given listing, or 0 if the
            number of available days does not exist
        '''
        if self.availability is None:
            print("Number of availability for this listing not available.")
            return 0
        return self.availability


def main():
    user = "qine"
    password = getpass.getpass()

    # Connect to the database
    query = DataSource()
    query.connect(user, password)

    # Query: host info
    # host_info = query.getHostInfo(2787)
    #
    # if host_info is not None:
    #     print("Host info query results (only showing price here): ")
    #     for item in host_info:
    #         print(item.getPrice())
    #
    # # Query: price
    # price = query.getPrice(5295)
    #
    # if price is not None:
    #     print("Price query results: ")
    #     for item in price:
    #         print(item)
    #
    # # Query: availability
    # availability = query.getAvailability(5295)
    #
    # if availability is not None:
    #     print("Availability info query results: ")
    #     for item in availability:
    #         print(item)
    '''
    num_reviews = query.getNumOfReviews(5295)
    if num_reviews is not None:
        print("Number of reviews for listing 5295 results:")
        for item in num_reviews:
            print(item)

    listings = query.getSameHouseType("Kensington", "Private room")
    if listings is not None:
        print("Listings in Kensington and roomtype is private: ")
        for item in listings:
            print(item)

    price_of_nei = query.getPriceOfNeighbourhood("Kensington")
    if price_of_nei is not None:
        print("prices of listings in Kensing are: ")
        for item in price_of_nei:
            print(item)

    single_listing = query.getListingInfo(5295)
    if single_listing is not None:
        print("listing info of 5295 is: ")
        for item in single_listing:
            print(item)

    num_of_listing = query.getNumOfListings("Brooklyn", "Private room")
    if num_of_listing is not None:
        print("Number of private rooms in Brooklyn is: ")
        for item in num_of_listing:
            print(item)

    sig_lst_pct = query.getHostSingleListingPct()
    if sig_lst_pct is not None:
        print("percentage of host having single listing is: ")
        for item in sig_lst_pct:
            print(item)

    #all_listing = query.getAllListings("Brooklyn", "Private room", (95, 150))
    
    single, multiple = query.getSingleMultipleListing()
    print(single)
    print(multiple)
    '''

    all_listing = query.getAllListings("Brooklyn", "Private room", (95, 150))


    # Disconnect from database
    query.disconnect()

main()
