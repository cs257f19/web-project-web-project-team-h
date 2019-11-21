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
            query = "SELECT * FROM airbnb where host_id = %s"
            cursor.execute(query, (str(host_id),))
            listing_tuples = cursor.fetchall()
            listings = [Listing(a_tuple) for a_tuple in listing_tuples]
            return listings
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
            query = "SELECT * FROM airbnb where neighbourhood = %s and room_type = %s"
            cursor.execute(query, (neighbourhood, room_type, ))
            listing_tuples = cursor.fetchall()
            listings = [Listing(a_tuple) for a_tuple in listing_tuples]
            return listings
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getAllListingOfType(self, room_type):
        '''
        Returns a list of listing objects of given room type.
        Helper function for self.getListingsForAllType()

        PARAMETERS:
            room_type - the listing space type

        RETURN:
            a list of listing objects with given room type or None if the query
            fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM airbnb where room_type = %s"
            cursor.execute(query, (room_type, ))
            listing_tuples = cursor.fetchall()
            listings = [Listing(a_tuple) for a_tuple in listing_tuples]
            return listings
        except Exception as e:
            print("Something went wrong when try to get listings for type:", e)
            return None

    def getListingsForAllType(self):
        '''
        Returns a dictionary containing 3 keys of all room types and lists of
        all listings of that room type using the helper function
        self.getAllListingOfType(room_type)
        Audience: tourists, researchers

        PARAMETERS:
            None

        RETURN:
            a dictionary containing 3 keys of all room types and lists of
            all listings of that room type
        '''
        result = {}
        result["Private"] = self.getAllListingOfType("Private room")
        result["Shared"] = self.getAllListingOfType("Shared room")
        result["Entire"] = self.getAllListingOfType("Entire home/apt")
        return result

    def getNumHostNumListing(self):
        '''
        Returns a dictionary using the number of listings as keys and number
        of hosts owning that number of listings as values
        Audience: researchers

        PARAMETERS:
            None

        RETURN:
            a dictionary using the number of listings as keys and number
            of hosts owning that number of listings as values or None if the
            query fails
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
        '''
        Returns a tuple with first entry as the number of hosts owning one listing,
        and second entry as the number of hosts owning multiple listings.
        Audience: reseacher

        PARAMETER:
            None

        RETURN:
            a tuple with first entry as the number of hosts owning one listing,
            and second entry as the number of hosts owning multiple listings,
            or None if the query fails
        '''
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
            if min_price > max_price:
                return 0
            query = "SELECT * FROM airbnb where neighbourhood_group = %s and" + \
                    " room_type = %s and price >= %s and price <= %s ORDER BY" + \
                    " number_of_reviews DESC"
            cursor.execute(query, (neighbourhood_group, room_type, str(min_price), str(max_price),))
            listing_tuples = cursor.fetchall()
            listings = [Listing(a_tuple) for a_tuple in listing_tuples]
            if len(listings) == 0:
                return 1
            return listings[:100]
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None

    def getAllAvailability(self):
        '''
        Returns a dictionary with 0 to 365 as keys indicating the availability
        of listings, and number of listings with that number of availability as
        values

        PARAMETERS:
            None

        RETURN:
            a dictionary with 0 to 365 as keys indicating the availability
            of listings, and number of listings with that number of availability
            as values or None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT availability_365 FROM airbnb"
            cursor.execute(query)
            result = cursor.fetchall()
            availability = {}
            for listing in result:
                listing_availability = listing[0]
                if listing_availability not in availability:
                    availability[listing_availability] = 0
                availability[listing_availability] += 1
            return availability
        except Exception as e:
            print("Something went wrong when getting availability for all:", e)
            return None

    def getNumListingPriceRange(self, min, max):
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(id) FROM airbnb where price > %s and price <= %s"
            cursor.execute(query, (str(min), str(max),))
            return cursor.fetchall()[0][0]
        except Exception as e:
            print("Something went wrong when getting the number of listings of certain prices:", e)
            return None

    def getPriceQuantile(self):
        listing_100 = self.getNumListingPriceRange(0,100)
        listing_200 = self.getNumListingPriceRange(100,200)
        listing_above = self.getNumListingPriceRange(200,10000000)
        return (listing_100, listing_200, listing_above)

    def getAverageAvailability(self):
        '''
        Returns the average available nights for all listings.
        Audience: investigators/researchers

        PARAMETERS:
            neighbourhood_group - one of the five boroughs of New York City
            room_type - the listing space type

        RETURN:
            the average available nights of all listings, or None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT AVG(availability_365) FROM airbnb"
            cursor.execute(query)
            average = float(cursor.fetchall()[0][0])
            return round(average, 2)
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None

    def getAverageNumOfReviews(self):
        '''
        Returns the average number of reviews for all listings.
        Audience: investigators/researchers

        PARAMETERS:
            None

        RETURN:
            the average number of reviews of all listings, or None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT AVG(number_of_reviews) FROM airbnb"
            cursor.execute(query)
            average = float(cursor.fetchall()[0][0])
            return round(average, 2)
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None

    def getAveragePrice(self):
        '''
        Returns the average price for listings.
        Audience: investigators/researchers, business owners

        PARAMETERS:
            None

        RETURN:
            the average price of listings, or None if the query fails
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT AVG(price) FROM airbnb"
            cursor.execute(query)
            average = float(cursor.fetchall()[0][0])
            return round(average, 2)
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None

    def getCertainRoomTypeCount(self, room_type):
        '''
        Helper function for getRoomTypeForAll(self)
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(id) FROM airbnb where room_type = %s"
            cursor.execute(query, (room_type,))
            return cursor.fetchall()[0][0]
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None

    def getTotalReviews(self):
        '''
        Returns the total number of reviews of all listings.

        PARAMETERS:
            None

        RETURNS:
            the total number of reviews of all listings, or None if the query
            fails

        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT SUM(number_of_reviews) FROM airbnb"
            cursor.execute(query)
            return cursor.fetchall()[0][0]
        except Exception as e:
            print("Something went wrong when executing the query:", e)
            return None

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

    '''
    listings = query.getSameHouseType("Kensington", "Private room")
    if listings is not None:
        print("Listings in Kensington and roomtype is private: ")
        for item in listings:
            print(item)

    sig_lst_pct = query.getHostSingleListingPct()
    if sig_lst_pct is not None:
        print("percentage of host having single listing is: ")
        for item in sig_lst_pct:
            print(item)
    '''
    all_listing = query.getAllListings("Brooklyn", "Private room", (20, 100))
    print(len(all_listing))

    '''
    single, multiple = query.getSingleMultipleListing()
    print(single)
    print(multiple)
    result = query.getListingsForAllType()
    length = len(result["Private"])
    print(length)
    '''
    #result = query.getNumListingPriceRange(300, float("inf"))
    #print(result)
    #result = query.getHostInfo(2787)
    #print(result)


    # Disconnect from database
    query.disconnect()

main()
