
var listings = new L.LayerGroup();
 var mymap = L.map('my_dataviz').setView([40.720610, -73.975242], 11);
 L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiemhhbmdzMTIzIiwiYSI6ImNrMXR6NjZobzAweW0zY3BrcnB4YmF6M3YifQ.nHmNai_UTcEJdy1VTbCXfg', {
   attribution: '',
   maxZoom: 18,
   id: 'mapbox.streets',
   accessToken: 'your.mapbox.access.token'
 }).addTo(mymap);
 var locations = [];
 {% for listing in results %}
 locations.push(["{{ listing.getListingName() }}", {{ listing.getLatitude() }}, {{ listing.getLongitude() }},
   "{{ listing.getListingName() }}","{{ listing.getListingId() }}","{{ listing.getPrice() }}","{{ listing.getMinNights() }}","{{ listing.getReviewsPerMonth() }}",
   "{{ listing.getNumAvailableDays() }}"])
{% endfor %}
 var arrLen = locations.length;
 var customOptions = {
   'maxWidth': '500',
   'className': 'custom'
 }
 for (var i = 0; i < locations.length; i++) {
   var customPopup = "<div class='popup'><h2><strong>"+locations[i][3]+"</strong></h2><p>listing id:"+locations[i][4]+"</p>" +
   "<p><u>$"+locations[i][7]+"</u>/night</p><p><u>"+locations[i][8]+"</u> night minimum</p>"  +
   "<p><u>"+locations[i][9]+"</u> reviews/month</p><p>Available <u>"+locations[i][10]+"</u> days"+"/year </p></div>";
   var marker = L.marker([locations[i][1],locations[i][2]]).addTo(mymap);
   marker.bindPopup(customPopup,customOptions);
 }
 mymap.addLayer(listings);
