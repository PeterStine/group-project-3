// Create a map object
let myMap = L.map("map", {
  center: [37.09, -95.71],
  zoom: 5
});

// Add a tile layer.
let baseMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMap);

// let jobData = L.layerGroup().addTo(myMap);

// Load the CSV data.
let geoData = "https://raw.githubusercontent.com/PeterStine/group-project-3/main/data/listings_cleaned.csv";



d3.csv(geoData).then(function (data) {
  // Create markers and add them to the layer group.

  markers = L.markerClusterGroup({
    showCoverageOnHover: false
  });

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
    }
    let listing = data[i];

    markers.addLayer(L.marker([listing.lat, listing.lon]))
      .bindPopup("<h2><a href=" + listing.url + " target = '_blank'>" + listing.title + "</a></h2>" + 
      "<h3>"+listing.company+"</h3>" +
      "<h3>"+listing.location+"</h3>" +
      "<h3>"+listing.salary+"</h3>" +
      "<h3>"+cleanOffice(listing.office)+"</h3>")

    // let listingMarker = L.marker([listing.lat, listing.lon])
    //   .bindPopup("<h2><a href=" + listing.url + " target = '_blank'>" + listing.title + "</a></h2>" + 
    //     "<h3>"+listing.company+"</h3>" +
    //     "<h3>"+listing.location+"</h3>" +
    //     "<h3>"+listing.salary+"</h3>" +
    //     "<h3>"+cleanOffice(listing.office)+"</h3>")

    // listingMarker.addTo(jobData);
  }

  myMap.addLayer(markers)
});


