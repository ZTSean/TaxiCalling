// This sample uses the Place Autocomplete widget to allow the user to search
// for and select a place. The sample then displays an info window containing
// the place ID and other information about the place that the user has
// selected.

// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
var mapId = "map";
var reportFreq = 20000; // default report frequency
var reqortHandle;
var driver1_path, driver2_path, driver3_path;
var driverMarkers = [], inforWindows = [];
var callerMarker, callerInfoWindow;
var bounds;
var map;


function initMap() {
    map = new google.maps.Map(document.getElementById(mapId), {
        center: {lat: 22.2823571, lng: 114.13887319999999},
        zoom: 15
    });

    // create Path for each driver ------------------------
    driver1_path = new google.maps.Polyline({
        path: [],
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2,
        map: map
    });

    driver2_path = new google.maps.Polyline({
        path: [],
        strokeColor: '#00FF00',
        strokeOpacity: 1.0,
        strokeWeight: 2,
        map: map
    });

    driver3_path = new google.maps.Polyline({
        path: [],
        strokeColor: '#0000FF',
        strokeOpacity: 1.0,
        strokeWeight: 2,
        map: map
    });

    //driver1_path.setMap(map);
    //driver2_path.setMap(map);
    //driver3_path.setMap(map);
    bounds = new google.maps.LatLngBounds();
    //-------------------------------------------------------
    // create marker for each driver
    for (i = 0; i < 3; i++) {
        let marker = new google.maps.Marker({
            map: map,
            icon: {
                url: "http://moziru.com/images/taxi-clipart-transparent-8.png",
                scaledSize: new google.maps.Size(48, 48)
            }
        });

        // add info window
        let infowindow = new google.maps.InfoWindow();
        marker.addListener('click', function () {
            infowindow.close();
            infowindow.open(map, marker);
        });

        driverMarkers.push(marker);
        inforWindows.push(infowindow);
    }

    callerMarker = new google.maps.Marker({
        map: map,
        icon: {
            url: "https://cdn1.iconfinder.com/data/icons/traveling-8/432/taxi-512.png",
            scaledSize: new google.maps.Size(48, 48)
        }
    });
    callerInfoWindow = new google.maps.InfoWindow();
    callerMarker.addListener('click', function () {
            callerInfoWindow.close();
            callerMarker.open(map, callerMarker);
        });

    //-------------------------------------------------------


    reportHandle = setInterval(update_routes, reportFreq);

    /*
    // traverse each driver's data & add marker with infowindow
    var tmp1 = {{ driverdata | safe }};

    var drivermakers = [];
    var callermakers = [];

    for (let i = 0; i < tmp1.length; i++) {
        //console.log(tmp[i]);
        let marker = new google.maps.Marker({
            map: map,
            position: {lat: tmp1[i]['location_lat'], lng: tmp1[i]['location_lng']},
            icon: {
                url: "http://moziru.com/images/taxi-clipart-transparent-8.png",
                scaledSize: new google.maps.Size(48, 48)
            }
        });

        // add info window
        let infowindow = new google.maps.InfoWindow();
        marker.addListener('click', function () {

            infowindow.close();
            infowindow.setContent(fillInfoWindowContentDriver(tmp1[i]));
            infowindow.open(map, marker);
        });

        drivermakers.push(marker);
    }
    for (let i = 0; i < tmp2.length; i++) {
        //console.log(tmp2[i]);
        let marker = new google.maps.Marker({
            map: map,
            position: {lat: tmp2[i]['from_lat'], lng: tmp2[i]['from_lng']},
            icon: {
                url: "https://cdn1.iconfinder.com/data/icons/traveling-8/432/taxi-512.png",
                scaledSize: new google.maps.Size(48, 48)
            }
        });

        // add info window
        let infowindow = new google.maps.InfoWindow();
        marker.addListener('click', function () {

            infowindow.close();
            infowindow.setContent(fillInfoWindowContentCaller(tmp2[i]));
            infowindow.open(map, marker);
        });

        drivermakers.push(marker);
    }
    */
}

/*
 entry.status
 entry.id
 entry.name
 */
function fillInfoWindowContentDriver(entry) {
    var status = "Available";
    if (entry.status == 2) status = "Hired";
    else if (entry.status == 3) status = "On-Call";

    var content = '<div id="infowindow-content">' +
        '<span id="driver-id" class="title">Driver ID: ' + entry.id + '</span><br>' +
        'Name: <span id="driver-name">' + entry.name + '</span><br>' +
        'Status: <span id="driver-status">' + status + '</span><br></div>';

    return content;
}

function fillInfoWindowContentCaller(entry) {

    var content = '<div id="infowindow-content">' +
        'Name: <span id="caller-name">' + entry.name + '</span><br>' +
        'Phone: <span id="caller-phone">' + entry.phone + '</span><br>' +
        'Location: <span id="caller-location">' + entry.location + '</span><br></div>';

    return content;
}

function update_routes() {
    $.ajax({
        url: '/callcentre', // form action url
        type: 'POST', // form submit method get/post
        dataType: 'json', // request type html/json/xml
        async: false,
        data: {"update" : 1}, // serialize form data
        success: function (feedback) {
            console.log("Success update driver paths request to the server...");
            console.log(feedback);

            var path = driver1_path.getPath();
            if (feedback.driver1_path_data.length > 1) {
                // update driver1 path
                for (let item in feedback.driver1_path_data) {
                    bounds.extend(new google.maps.LatLng(item.lat, item.lng));
                }
                driver1_path.setPath(feedback.driver1_path_data);

                // update driver 1 marker
                driverMarkers[0].setPosition(new google.maps.LatLng(feedback.driver1_path_data[0].lat, feedback.driver1_path_data[0].lng));

                // update driver 1 infowindows
                inforWindows[0].setContent(fillInfoWindowContentDriver({
                    status: feedback.driver1_status,
                    id: 1,
                    name: "Driver 1"
                }));
            }

            path = driver2_path.getPath();
            if (feedback.driver2_path_data.length > 1) {
                // update driver2 path
                for (let item in feedback.driver2_path_data) {
                    bounds.extend(new google.maps.LatLng(item.lat, item.lng));
                }
                driver2_path.setPath(feedback.driver2_path_data);

                // update driver 2 marker
                driverMarkers[1].setPosition(new google.maps.LatLng(feedback.driver2_path_data[0].lat, feedback.driver2_path_data[0].lng));

                // update driver 2 infowindows
                inforWindows[1].setContent(fillInfoWindowContentDriver({
                    status: feedback.driver2_status,
                    id: 2,
                    name: "Driver 2"
                }));
            }

            path = driver3_path.getPath();
            if (feedback.driver3_path_data.length > 1) {
                // update driver3 path
                for (let item in feedback.driver3_path_data) {
                    bounds.extend(new google.maps.LatLng(item.lat, item.lng));
                }
                driver3_path.setPath(feedback.driver3_path_data);

                // update driver 3 marker
                driverMarkers[2].setPosition(new google.maps.LatLng(feedback.driver3_path_data[0].lat, feedback.driver3_path_data[0].lng));

                // update driver 3 infowindows
                inforWindows[2].setContent(fillInfoWindowContentDriver({
                    status: feedback.driver3_status,
                    id: 3,
                    name: "Driver 3"
                }));
            }

            callerMarker.setPosition(new google.maps.LatLng(feedback.caller.from_lat, feedback.caller.from_lng));
            callerInfoWindow.setContent(fillInfoWindowContentCaller({
                    name: feedback.caller.name,
                    phone: feedback.caller.phone,
                    location: feedback.caller.from_lat + "," + feedback.caller.from_lng

                }));

            map.fitBounds(bounds);

        },
        error: function (e) {
            $("#modal-feedback-title").html("Invalid Request");
            $("#modal-feedback").html(e);
            $("#myModal").modal("show");
        }
    });
}




