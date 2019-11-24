import flask
from flask import render_template,request
import json
import sys
sys.path.append('../Backend/')
from datasource import *

app= flask.Flask(__name__)

@app.route('/script.js')
def script(results):
    return render_template('searchResult.js', results=results)

@app.route('/')
def homePage():
    '''
    Renders the home page.

    PARAMETERS:
        None

    RETURNS:
        render homePage.html
    '''
    return render_template('homePage.html')

@app.route('/data')
def dataPage():
    '''
    Renders the "About Data" page.

    PARAMETERS:
        None

    RETURNS:
        render dataPage.html
    '''
    return render_template('dataPage.html')

@app.route('/hostSearch')
def hostSearch():
    '''
    Renders the "For Host" search page.

    PARAMETERS:
        None

    RETURNS:
        render hostSearch.html
    '''
    return render_template('hostPage.html')

@app.route('/listingSearch')
def listingSearch():
    '''
    Renders the "Listing Search" page.

    PARAMETERS:
        None

    RETURNS:
        render hostSearch.html
    '''
    return render_template('searchPage.html')

@app.route('/errorPage')
def errorPage(msg):
    '''
    Renders the error page with desired message.

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
    it renders the "For Host" search result page when the host id input is
    valid. Otherwise, it renders the error page.

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
        host_info = db.getHostInfo(host_id)

        if not host_info:
            return errorPage('Please enter a valid host id!')

        return render_template('hostResult.html',results=host_info, database=db)

@app.route('/listingResult',methods = ['POST', 'GET'])
def listingResult():
    '''
    This function get called when the search button is clicked on
    searchPage.html, it renders the "Listing Search" result page when the inputs
    are all valid and there are listings found for the given criterion.
    Otherwise, it renders error page with descriptive messages.

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
        min_price = int(result['min price'])
        max_price = int(result['max price'])
        nbh_group = result['neighborhood group']
        room_type = result['room type']

        # initialize data source object
        db = DataSource()
        db.connect('qine', 'ruby434seal')

        listings = db.getAllListings(nbh_group, room_type, (min_price, max_price))

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
    Renders the "Visualize Data" page that gives the overall statistics. 

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
