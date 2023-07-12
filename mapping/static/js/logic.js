// Creating the map object
let myMap = L.map("map", {
    center: [39.82869195347417, -98.57935095398236],
    zoom: 5
  });

  // Adding the tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMap);

// Load the GeoJSON data.
let geoData = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";

d3.json(geoData).then(function(data) {

    console.log(data);

    for (let i = 0; i < data.features.length; i++) {
        // Check that magnitude is not Null
        if(data.features[i].properties.mag >= 0) {
            createMark(data.features[i])
        }
    };

});

function markerColor(param1) {
    if (-10 <= param1 && param1 < 10) {
        return "darkgreen"
    }

    else if (10 <= param1 && param1 < 30) {
        return "green"
    }

    else if (30 <= param1 && param1 < 50) {
        return "lightgreen"
    }

    else if (50 <= param1 && param1 < 70) {
        return "orange"
    }

    else if (70 <= param1 && param1 < 90) {
        return "#F8836A"
    }

    else {
        return "red"
    };

};

function createMark(feature) {
    // Create a circle, and pass in some initial options.
    let latitude = feature.geometry.coordinates[1];
    let longitude = feature.geometry.coordinates[0];
    let depth = feature.geometry.coordinates[2];

    let magnitude = feature.properties.mag;
    let markerSize = magnitude * 7500;

    let location = [latitude, longitude];
    let time = new Date(feature.properties.time);
    let dateFormat = time.getHours() + ":" + time.getMinutes() + ", " + time.toDateString();

    let newMark = L.circle(location, {
            color: "black",
            weight: 0.5,
            fillColor: markerColor(depth),
            fillOpacity: 0.75,
            radius: markerSize
        }).addTo(myMap);

    newMark.bindPopup("<b>Magnitude: <b>" + magnitude + "<br> <b>Location: <b>" + feature.properties.place + 
    "<br> <b>Longitude: <b>" + longitude +  "<br> <b>Latitude: <b>" + latitude + "<br> <b>Time: <b>" + dateFormat
    + "<br> <b>Depth (km): <b>" + depth)
};

/*I found this code online, but it's just putting text on the page, no box or colors displayed*/
var legend = L.control({ position: "bottomright" });
legend.onAdd = function(map) {
  var div = L.DomUtil.create("div", "legend");
  div.innerHTML += "<h4>Depth in kilometers</h4>";
  div.innerHTML += '<i style="background: darkgreen"></i><span>-10 - 10</span><br>';
  div.innerHTML += '<i style="background: green"></i><span>10 - 30</span><br>';
  div.innerHTML += '<i style="background: lightgreen"></i><span>30 - 50</span><br>';
  div.innerHTML += '<i style="background: orange"></i><span>50 - 70</span><br>';
  div.innerHTML += '<i style="background: #F8836A"></i><span>70 - 90</span><br>';
  div.innerHTML += '<i style="background: red"></i><span>> 90</span><br>';
  
  return div;
};

legend.addTo(myMap);
