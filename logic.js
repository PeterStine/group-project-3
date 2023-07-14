// Create a map object
let myMap = L.map("map", {
  center: [37.09, -95.71],
  zoom: 5
});

// Add a tile layer.
let baseMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMap);

let jobData = L.layerGroup().addTo(myMap);

// Load the CSV data.
let geoData = "listings_cleaned.csv";



d3.csv(geoData).then(function (data) {
  console.log(data);

  // Create markers and add them to the layer group.
  for (let i = 0; i < data.length; i++) {
    let listing = data[i];
    let listingMarker = L.marker([listing.lat, listing.lon]).bindPopup("<h3>" + listing.company + listing.salary + listing.url + listing.title + "</h3>");

    // Add an event listener to the marker's click event.
    listingMarker.on("click", function () {
      // Retrieve the URL you want to navigate to from the marker's data.
      let url = listing.url;

      // Create a link element and simulate a click to navigate to the URL.
      let link = document.createElement("a");
      link.href = url;
      link.target = "_blank";
      link.click();
    });

    listingMarker.addTo(jobData);
  }
});





// d3.csv(geoData).then(function (data) {
//   console.log(data);

//   // Create markers and add them to the layer group.
//   for (let i = 0; i < data.length; i++) {
//     let listing = data[i];
//     let listingMarker = L.marker([listing.lat, listing.lon]).bindPopup("<h3>" + listing.company + listing.salary + listing.url + listing.title + "</h3>");

//     // Add an event listener to the marker's popupopen event or click event.
//     listingMarker.on("popupopen", function () {
//       // Retrieve the URL you want to navigate to from the marker's data.
//       let url = listing.url;

//       // Navigate to the URL using window.location.href.
//       window.location.href = url;
//     });

//     listingMarker.addTo(jobData);
//   }
// });




// d3.csv(geoData).then(function (data) {
//   console.log(data);

//   function createMarkers(response) {
//     let listings = data;
//     let listingMarkers = [];
//     for (let i = 0; i < listings.length; i++) {
//       let listing = listings[i];
//       let listingMarker = L.marker([listing.lat, listing.lon]).bindPopup("<h3>" + listing.company + listing.salary + listing.url + listing.title + "</h3>");
//       listingMarker.addTo(jobData);

//       // Add the marker-animation class to each marker.
//       listingMarker.getElement().classList.add("marker-animation");

//       listingMarkers.push(listingMarker);
//     }
//     console.log(listingMarkers);
//   }

//   createMarkers(data);

//   jobData.addTo(myMap);
// });



