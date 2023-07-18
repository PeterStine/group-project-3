// Create a map object
let myMap = L.map("map", {
  center: [37.09, -95.71],
  zoom: 5
});

// Add a tile layer.
let baseMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMap);

// Create overlay layers
let jobData = L.layerGroup().addTo(myMap);
let inPerson = L.layerGroup().addTo(myMap);
let hybrid = L.layerGroup().addTo(myMap);
let remote = L.layerGroup().addTo(myMap);

let markers = L.markerClusterGroup({
  showCoverageOnHover: false
});

// Load the CSV data.
let geoData = "https://raw.githubusercontent.com/PeterStine/group-project-3/main/data/listings_cleaned.csv";

d3.csv(geoData).then(function (data) {
  // Create markers and add them to the layer group.

  for (let i = 0; i < data.length; i++) {

    function cleanOffice(officeType){
      switch (true) {
        case officeType == "in_person":
          return "In Person"
        case officeType == "hybrid":
          return "Hybrid"
        case officeType == "remote":
          return "Remote"
      }
    };
    let listing = data[i];

    // Add marks for cluster map
    let clusterMarker = (L.marker([listing.lat, listing.lon]))
      .bindPopup("<h2><a href=" + listing.url + " target = '_blank'>" + listing.title + "</a></h2>" + 
      "<h3>"+listing.company+"</h3>" +
      "<h3>"+listing.location+"</h3>" +
      "<h3>"+listing.salary+"</h3>" +
      "<h3>"+cleanOffice(listing.office)+"</h3>")

    clusterMarker.addTo(markers);
       
    // Add marks for all listings
    let listingMarker = L.marker([listing.lat, listing.lon])
      .bindPopup("<h2><a href=" + listing.url + " target = '_blank'>" + listing.title + "</a></h2>" + 
        "<h3>"+listing.company+"</h3>" +
        "<h3>"+listing.location+"</h3>" +
        "<h3>"+listing.salary+"</h3>" +
        "<h3>"+cleanOffice(listing.office)+"</h3>")

    listingMarker.addTo(jobData);

    // Add marks only for in_person listings
    if (listing.office == 'in_person') {
      let inPersonMarker = L.marker([listing.lat, listing.lon])
        .bindPopup("<h2><a href=" + listing.url + " target = '_blank'>" + listing.title + "</a></h2>" + 
          "<h3>"+listing.company+"</h3>" +
          "<h3>"+listing.location+"</h3>" +
          "<h3>"+listing.salary+"</h3>" +
          "<h3>"+cleanOffice(listing.office)+"</h3>")

      inPersonMarker.addTo(inPerson);
    };

    // Add marks only for hybrid listings
    if (listing.office == 'hybrid') {
      let hybridMarker = L.marker([listing.lat, listing.lon])
        .bindPopup("<h2><a href=" + listing.url + " target = '_blank'>" + listing.title + "</a></h2>" + 
          "<h3>"+listing.company+"</h3>" +
          "<h3>"+listing.location+"</h3>" +
          "<h3>"+listing.salary+"</h3>" +
          "<h3>"+cleanOffice(listing.office)+"</h3>")

      hybridMarker.addTo(hybrid);
    };

    // Add marks only for remote listings
    if (listing.office == 'remote') {
      let remoteMarker = L.marker([listing.lat, listing.lon])
        .bindPopup("<h2><a href=" + listing.url + " target = '_blank'>" + listing.title + "</a></h2>" + 
          "<h3>"+listing.company+"</h3>" +
          "<h3>"+listing.location+"</h3>" +
          "<h3>"+listing.salary+"</h3>" +
          "<h3>"+cleanOffice(listing.office)+"</h3>")

      remoteMarker.addTo(remote);
    };

  };  
});

// Overlay choice between cluster markers and all individual job listings
let overlayMaps = {
  "All Listings": jobData,
  "In Person": inPerson,
  "Hybrid": hybrid,
  "Remote": remote,
  "Cluster Map": markers,
};

// Pass our map layers into our layer control.
// Add the layer control to the map.
L.control.layers(overlayMaps).addTo(myMap);


