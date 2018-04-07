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

    console.log("Your current location: " + geolocation.lat + " " + geolocation.lng);
    console.log(document.getElementById("driver-location_lat").value != geolocation.lat);

    
    // if the location data is not consistent with previous one 
    if (document.getElementById("driver-location_lat").value != geolocation.lat ||
    document.getElementById("driver-location_lng").value != geolocation.lng ) {
        document.getElementById("driver-location_lat").value == geolocation.lat;
        document.getElementById("driver-location_lng").value == geolocation.lng;

        document.getElementById("lat").value = geolocation.lat.toFixed(7);
        document.getElementById("lng").value = geolocation.lng.toFixed(7);
        //document.getElementById("lat").value = geolocation.lat.toFixed(7) + " " + count;
        //document.getElementById("lng").value = geolocation.lng.toFixed(7) + " " + count;
        
        console.log("information need to update: submit form");
        
        // --------------------------------------------------
        //submitForm();

        // filling the form
        var now = new Date();
        var date = now.toISOString().slice(0, 19).replace('T', ' ').split(" ");

        console.log($('form').serialize());
        $.ajax({
            url: '/update_driver_location', // form action url
            type: 'POST', // form submit method get/post
            dataType: 'html', // request type html/json/xml
            async:false,
            data: $('#form-driver-status').serialize(), // serialize form data 
            success: function(data) {
                console.log("Success send driver real time location data to the server...");

                feedback = JSON.parse(data);
                console.log(feedback.status == "INVALID_REQUEST");
                if (feedback.status == "INVALID_REQUEST") {
                    error_message = "Invalid Request:<br />";

                    $("#modal-feedback-title").html("Invalid Request");
                    $("#modal-feedback").html(error_message);
                    $("#myModal").modal("show");


                } else if (feedback.status == "OK") {
                    if (feedback.update == 2) { // driver get hired
                        $("#modal-feedback-title").html("Congrats!");
                        $("#modal-feedback").html("You have been on-call!");
                        $("#myModal").modal("show");

                        // show the on-call button
                        $("#btn-pick-up").show();
                    }
                }
            },
            error: function(e) {
                $("#modal-feedback").html(e);
                $("#myModal").modal("show");
            }
        });

        // refill the form
        document.getElementById("driver-date").value = date[0];
        document.getElementById("driver-time").value = date[1];
        document.getElementById("driver-location_lat").value = geolocation.lat;
        document.getElementById("driver-location_lng").value = geolocation.lng;
        document.getElementById("lat").value = geolocation.lat.toFixed(7);
        document.getElementById("lng").value = geolocation.lng.toFixed(7);

        if (reportFreq == 30000) document.getElementById("report_3_min") == true;
        if (reportFreq == 10000) document.getElementById("report_1_min") == true;
        //document.getElementById("");
    }
    
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