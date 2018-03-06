// This sample uses the Place Autocomplete widget to allow the user to search
// for and select a place. The sample then displays an info window containing
// the place ID and other information about the place that the user has
// selected.

// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

var mapId = "map";
var map;
var curLocationMarker;
var infowindow;
var count = 0;


function initMap() {
    map = new google.maps.Map(document.getElementById(mapId), {
        center: { lat: 22.2823571, lng: 114.13887319999999 },
        zoom: 15
    });

    // current location marker
    infowindow = new google.maps.InfoWindow();

    curLocationMarker = new google.maps.Marker({
        map: map
    });

    curLocationMarker.addListener('click', function() {
        infowindow.open(map, curLocationMarker);
    });
}

function geolocate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        console.log("Browser does support geolocation.");
    }
}

function showPosition(position) {
    curLocationMarker.setVisible(false);
    infowindow.close();
    count += 1;

    var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };

    curLocationMarker.setPosition(geolocation);
    curLocationMarker.setVisible(true);

    //reset map center
    map.setOptions({
        center: geolocation,
        zoom: 15
    });

    infowindow.setContent("<div>Your current location: <div>" + geolocation.lat + " " + geolocation.lng);
    infowindow.open(map, curLocationMarker);

    // submit to the database
    document.getElementById("lat").value = geolocation.lat.toFixed(4) + " " + count;
    document.getElementById("lng").value = geolocation.lng.toFixed(4) + " " + count;

    console.log("Your current location: " + geolocation.lat + " " + geolocation.lng);
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            console.log("User denied the request for Geolocation.");

            break;
        case error.POSITION_UNAVAILABLE:
            console.log("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            console.log("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            console.log("An unknown error occurred.");
            break;
    }
}

