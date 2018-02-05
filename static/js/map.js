// This sample uses the Place Autocomplete widget to allow the user to search
// for and select a place. The sample then displays an info window containing
// the place ID and other information about the place that the user has
// selected.

// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
var searchInputId = "pac-input";
var mapId = "map";
var curLocationMarker;

function initMap() {
    var map = new google.maps.Map(document.getElementById(mapId), {
        center: {lat: 22.2823571, lng: 114.13887319999999},
        zoom: 15
    });

    // Create the search box and link it to the UI element.
    var input = document.getElementById(searchInputId);

    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    var infoWindowContent = '<div class="info_content">' +
        '<h3>London Eye</h3>' +
        '<p>The London Eye is a giant Ferris wheel situated on the banks of the River Thames. The entire structure is 135 metres (443 ft) tall and the wheel has a diameter of 120 metres (394 ft).</p>' +
        '</div>';

    var infowindow = new google.maps.InfoWindow();
    var marker = new google.maps.Marker({
        map: map
    });
    marker.addListener('click', function () {
        infowindow.open(map, marker);
    });

    // current location marker
    curLocationMarker = new google.maps.Marker({
        map: map
    });

    // initialize autocomplete
    initAutocomplete(searchInputId, map, infowindow, marker);
}

function initAutocomplete(searchInputId, map, infowindow, marker) {
    // Create the autocomplete object, restricting the search to geographical
    // location types.
    autocomplete = new google.maps.places.Autocomplete(
        /** @type {!HTMLInputElement} */(document.getElementById(searchInputId)),
        {types: ['geocode']});

    autocomplete.bindTo('bounds', map);

    // When the user selects an address from the dropdown, populate the address
    // fields in the form.
    autocomplete.addListener('place_changed', function () {
        console.log("place changed.");
        showInfoWindow(map, infowindow, marker);
        //fillInAddress(); has been done in showInfoWindow
    });
}

function showInfoWindow(map, infowindow, marker) {
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();

    // ========================== Show the address info on the map ===============================
    // close infowindow & hide marker when new search starts
    infowindow.close();
    marker.setVisible(false);

    // deal with the information from the search
    if (!place.geometry) {
        // User entered the name of a Place that was not suggested and
        // pressed the Enter key, or the Place Details request failed.
        window.alert("No details available for input: '" + place.name + "'");
        return;
    }

    // If the place has a geometry, then present it on a map.
    if (place.geometry.viewport) {
        map.fitBounds(place.geometry.viewport);
    } else {
        map.setCenter(place.geometry.location);
        map.setZoom(17); // Why 17? Because it looks good.
    }

    // Set the position of the marker using the place ID and location.
    marker.setPlace({
        placeId: place.place_id,
        location: place.geometry.location
    });
    marker.setVisible(true);

    document.getElementById('place-name').textContent = place.name;
    document.getElementById('place-id').textContent = place.place_id;
    document.getElementById('place-address').textContent = place.formatted_address;

    // fill the location info into the form, which will be submitted
    document.getElementById('call-taxi-address').value = place.formatted_address;
    document.getElementById('call-taxi-to_x').value = place.geometry.location.lat();
    document.getElementById('call-taxi-to_y').value = place.geometry.location.lng();
    console.log("Fill the addr:" + document.getElementById('call-taxi-address').value + " " +
        document.getElementById('call-taxi-to_x').value + " "
        + document.getElementById('call-taxi-to_y').value
    );

    infowindow.setContent(fillInfoWindowContent(place.name, place.id, place.formatted_address));
    infowindow.open(map, marker);
}

function fillInfoWindowContent(name, id, address) {
    var content = '<div id="infowindow-content">' +
        '<span id="place-name" class="title">' + name + '</span>' +
        '<br>' +
        'Place ID: <span id="place-id">' + id + '</span>' +
        '<br>' +
        '<span id="place-address">' + address + '</span><br>' +
        '<button class="btn btn-primary btn-sm">Confirm</button>' +
        '</div>';

    return content;
}

function fillInAddress() {
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();

    console.log(place);
    // ========================== filling the form ===============================
    /*
    for (var component in componentForm) {
        document.getElementById(component).value = '';
        document.getElementById(component).disabled = false;
    }

    // Get each component of the address from the place details
    // and fill the corresponding field on the form.
    for (var i = 0; i < place.address_components.length; i++) {
        var addressType = place.address_components[i].types[0];
        if (componentForm[addressType]) {
            var val = place.address_components[i][componentForm[addressType]];
            document.getElementById(addressType).value = val;
        }
    }*/


}

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    }
}


function showPosition(position) {
    var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };

    /*
    var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
    });
    autocomplete.setBounds(circle.getBounds());
    */
    curLocationMarker.setPosition(geolocation);
    curLocationMarker.setVisible(true);

    // get current location
    document.getElementById('call-taxi-from_x').value = geolocation.lat;
    document.getElementById('call-taxi-from_y').value = geolocation.lng;
    console.log("Current location: " +
        document.getElementById('call-taxi-from_x').value + " "
        + document.getElementById('call-taxi-from_y').value
    );
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            console.log("User denied the request for Geolocation.");
            // clear from_x & from_y
            document.getElementById('call-taxi-from_x').value = "";
            document.getElementById('call-taxi-from_y').value = "";

            break;
        case error.POSITION_UNAVAILABLE:
            console.log("Location information is unavailable.");
            // clear from_x & from_y
            document.getElementById('call-taxi-from_x').value = "";
            document.getElementById('call-taxi-from_y').value = "";
            break;
        case error.TIMEOUT:
            console.log("The request to get user location timed out.");
            // clear from_x & from_y
            document.getElementById('call-taxi-from_x').value = "";
            document.getElementById('call-taxi-from_y').value = "";
            break;
        case error.UNKNOWN_ERROR:
            console.log("An unknown error occurred.");
            // clear from_x & from_y
            document.getElementById('call-taxi-from_x').value = "";
            document.getElementById('call-taxi-from_y').value = "";
            break;
    }
}