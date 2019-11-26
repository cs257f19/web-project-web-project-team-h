import flask
from flask import render_template,request
import json
import sys
sys.path.append('../Backend/')
from datasource import *

app= flask.Flask(__name__)

@app.route('/')
def homePage():
    '''
    Renders the home page of the entire project about Airbnb in NYC.
    Audience: all

    PARAMETERS:
        None

    RETURNS:
        render homePage.html
    '''
    return render_template('homePage.html')

@app.route('/data')
def dataPage():
    '''
    Renders the "About Data" page that includes metadata and description of the
    entire dataset. There are also some example data on this page.
    Audience: all

    PARAMETERS:
        None

    RETURNS:
        render dataPage.html
    '''
    return render_template('dataPage.html')

@app.route('/hostSearch')
def hostSearch():
    '''
    Renders the "For Host" search page that asks hosts to enter their airbnb
    host id. Note that non-hosts can test the page by using the host id examples
    we give on the "about data" page. Once valid host id is entered, the search
    will take place and redirect the user to the host search result page.
    Audience: hosts

    PARAMETERS:
        None

    RETURNS:
        render hostSearch.html
    '''
    return render_template('hostPage.html')

@app.route('/listingSearch')
def listingSearch():
    '''
    Renders the "Listing Search" page that allows tourists to search for
    housing of interest by asking them for ideal price range, neighborhood
    group, and room type. Once valid criterion are inputted, the search will
    happen and redirect the user to the listing search result page.
    Audience: tourists

    PARAMETERS:
        None

    RETURNS:
        render hostSearch.html
    '''
    return render_template('searchPage.html')

@app.route('/errorPage')
def errorPage(msg):
    '''
    Renders the error page that displays a descriptive message according
    to the error made by the user and/or the system.
    Audience: all

    PARAMETERS:
        msg: a string of message that will be displayed on the error page

    RETURNS:
        render errorPage.html with a display of the message
    '''
    return render_template('errorPage.html', msg=msg)

@app.route('/hostResult',methods = ['POST', 'GET'])
def hostResult():
    '''
    This function get called when the submit button is clicked on hostPage.html,
    it renders the "For Host" search result page that displays relevant
    information of their listings and listings of the same room type in the same
    neighborhood. This allows hosts to learn more about the competitions
    associated with their listings. If the host id input is not valid, it
    renders the error page.
    Audience: hosts

    PARAMETERS:
        None

    RETURNS:
        render hostResult.html with the host id entered by user in
        hostSearch.html entered in hostPage.html and a datasource object
    '''
    if request.method == 'POST':
        result = request.form
        db = DataSource()
        db.connect('qine', 'ruby434seal')
        host_id = result['id']
        host_info = db.getHostListings(host_id)

        if not host_info:
            return errorPage('Please enter a valid host id!')

        return render_template('hostResult.html',results=host_info, database=db)

@app.route('/listingResult',methods = ['POST', 'GET'])
def listingResult():
    '''
    This function get called when the search button is clicked on
    searchPage.html, it renders the "Listing Search" result page that shows the
    listings that satisfy the search criterion on a map. If there are more than
    100 listings found, we only display the first 100 listings with the most
    reviews. If the inputs are not all valid or if there is no listing found
    for the given criterion, it renders error page with descriptive messages.
    Audience: tourists

    PARAMETERS:
        None

    RETURNS:
        render the searchResult.html page with a list of listings that
        satisfy the conditions entered by the user in searchPage.html
    '''
    if request.method == 'POST':
        result = request.form

        # check for valid user input
        if not result['min price'] or not result['max price']:
            return errorPage('Please enter values for both min and max price.')
        if 'neighborhood group' not in result or 'room type' not in result:
            return errorPage('Please select a neighborhood group and a room type.')

        # get user input from searchPage.html
        min_price = int(float(result['min price']))
        max_price = int(float(result['max price']))
        nbh_group = result['neighborhood group']
        room_type = result['room type']

        # initialize data source object
        db = DataSource()
        db.connect('qine', 'ruby434seal')

        listings = db.getListingsSearchResult(nbh_group, room_type, (min_price, max_price))

        # display error pages for edge cases
        if not listings:
            return errorPage('Please make sure all your inputs are correct!')
        elif listings == 1:
            return errorPage('Please make sure min price is less than or equal to max price!')
        elif listings == 2:
            return errorPage('No listings are found for your criterion.')

        return render_template('searchResult.html', results=listings)

@app.route('/overall')
def overall():
    '''
    Renders the "Visualize Data" page that provides visualizations for the
    overall statistics of the NYC Airbnb data. This gives researchers and
    investigators a good overall understanding of how Airbnb performs in
    NYC in general
    Audience: researchers and investigators

    PARAMETERS:
        None

    RETURNS:
        render overallPage.html with the needed information for researchers
        and investigators.
    '''
    # initialize data source object
    db = DataSource()
    db.connect('qine', 'ruby434seal')

    # get information for the 'Activity' section on overallPage.html
    average_reviews_per_month = round(db.getAverageNumOfReviews()/12, 2)
    total_reviews = db.getTotalReviews()
    average_price = db.getAveragePrice()
    price_dict = db.getPriceQuantile()

    # get information for the 'Availability' section on overallPage.html
    average_availability = db.getAverageAvailability()
    availability_dict = db.getAllAvailability()

    # get information for the 'Room Type' section on overallPage.html
    entire_home_count = db.getCertainRoomTypeCount('Entire home/apt')
    private_room_count = db.getCertainRoomTypeCount('Private room')
    shared_room_count = db.getCertainRoomTypeCount('Shared room')

    # get information for the 'Listings Per Host' section on overallPage.html
    host_listings = db.getNumHostNumListing()
    single_multiple_listings = db.getSingleMultipleListing()
    host_single_count = single_multiple_listings[0]
    host_multiple_count = single_multiple_listings[1]

    # get information for the 'Average Neighborhood Group Price' section on overallPage.html
    nbh_group_avg_price = db.getAveragePriceNbhGroup()

    return render_template('overallPage.html',
                            average_reviews_per_month=average_reviews_per_month,
                            total_reviews=total_reviews,
                            average_price=average_price,
                            price_dict=price_dict,
                            average_availability=average_availability,
                            availability_dict=availability_dict,
                            entire_home_count=entire_home_count,
                            private_room_count=private_room_count,
                            shared_room_count=shared_room_count,
                            host_listings=host_listings,
                            host_single_count=host_single_count,
                            host_multiple_count=host_multiple_count,
                            nbh_group_avg_price=nbh_group_avg_price)

if __name__=='__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()
    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port, debug=True)
