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
    Return homePage.html
    '''
    return render_template('homePage.html')

@app.route('/data')
def dataPage():
    '''
    Return dataPage.html
    '''
    return render_template('dataPage.html')

@app.route('/hostSearch')
def hostSearch():
    '''
    Return hostSearch.html
    '''
    return render_template('hostPage.html')

@app.route('/listingSearch')
def listingSearch():
    '''
    Return hostSearch.html
    '''
    return render_template('searchPage.html')

@app.route('/hostResult',methods = ['POST', 'GET'])
def hostResult():
    '''
    Get called when the submit button is clicked on hostPage.html
    Return homeResult.html with data entered in hostPage.html
    '''
    if request.method == 'POST':
        result = request.form
        db = DataSource()
        db.connect('qine', 'ruby434seal')
        host_id = result['id']
        host_info = db.getHostInfo(host_id)
        return render_template('hostResult.html',results=host_info, database=db)

@app.route('/listingResult',methods = ['POST', 'GET'])
@app.route('/listingResult')
def listingResult():
    '''
    Return listingResult.html
    '''
    if request.method == 'POST':
        result = request.form
        host_id = result['id']
        min_price = result['min price']
        max_price = result['max price']
        nbh_group = result['neighborhood group']
        room_type = result['room type']
        price_range = (min_price, max_price)

        db = DataSource()
        db.connect('qine', 'ruby434seal')
        listings = db.getAllListings(nbh_group, room_type, price_range)
        return render_template('searchResult.html', results=listings, database=db)

@app.route('/overall')
def overall():
    '''
    Return overallPage.html
    '''
    db = DataSource()
    db.connect('qine', 'ruby434seal')

    average_reviews_per_month = db.getAverageNumOfReviews()/12
    total_reviews = db.getTotalReviews()
    average_price = db.getAveragePriceNbh()

    average_availability = db.getAverageAvailability()

    entire_home_count = db.getCertainRoomTypeCount('Entire home/apt')
    private_room_count = db.getCertainRoomTypeCount('Private room')
    shared_room_count = db.getCertainRoomTypeCount('Shared room')

    host_listings = db.getNumHostNumListing()
    single_multiple_listings = db.getSingleMultipleListing()
    host_single_count = single_multiple_listings[0]
    host_multiple_count = single_multiple_listings[1]

    return render_template('overallPage.html', database=db,
                            average_reviews_per_month, total_reviews,
                            average_price, average_availability,
                            entire_home_count, private_room_count,
                            shared_room_count, host_listings, host_single_count,
                            host_multiple_count)

if __name__=='__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()
    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port, debug=True)
