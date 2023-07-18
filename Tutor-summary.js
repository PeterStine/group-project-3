//Create a map object
let myMap = L.map("map", {
    center: [37.09, -95.71],
    zoom: 5
});

// Add a tile layer.
let baseMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMap);

let jobData = new L.LayerGroup();
//L.control.layer(baseMap, jobData).addTo(myMap);
// Load the GeoJSON data.
let geoData = "listings_cleaned.csv";

d3.csv(geoData).then(function (data) {

    console.log(data);
    function createMarkers(response) {
        let listings = data;
        let listingMarkers = [];
        for (let i = 0; i < listings.length; i++) {
            let listing = listings[i];
            
            let listingMarker = L.marker([listing.lat, listing.lon]).bindPopup("<h3>" + listing.company);
            //console.log(listingMarker);
            listingMarkers.push(listingMarker)   //.addTo(jobData);
        }
        console.log(listingMarkers); 
    }
    //console.log(listingMarkers);
    jobData.addTo(myMap);
});