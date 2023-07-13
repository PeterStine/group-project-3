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
let geoData = "../data/listings_cleaned.csv";

d3.csv(geoData).then(function(data) {

    console.log(data);

    // for (let i = 0; i < data.features.length; i++) {
    //     // Check that magnitude is not Null
    //     if(data.features[i].properties.mag >= 0) {
    //         createMark(data.features[i])
    //     }
    // };

});