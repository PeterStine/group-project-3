// Create a map object
let myMap = L.map("map", {
  center: [37.09, -95.71],
  zoom: 5
});

// Add a tile layer
let baseMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(myMap);

// Create overlay layers
let jobData = L.layerGroup().addTo(myMap);
let inPerson = L.layerGroup().addTo(myMap);
let hybrid = L.layerGroup().addTo(myMap);
let remote = L.layerGroup().addTo(myMap);

// Create a cluster marker group
let markers = L.markerClusterGroup({
  showCoverageOnHover: false
});

// Load the CSV data
let geoData = "https://raw.githubusercontent.com/PeterStine/group-project-3/main/data/listings_cleaned.csv";

d3.csv(geoData).then(function (data) {
  // Create markers and add them to the appropriate layer groups
  let states = [];
  for (let i = 0; i < data.length; i++) {
    function cleanOffice(officeType) {
      switch (officeType) {
        case "in_person":
          return "In Person";
        case "hybrid":
          return "Hybrid";
        case "remote":
          return "Remote";
      }
    }

    let listing = data[i];
    states.push(listing.location);

    // Create a cluster marker
    let clusterMarker = L.marker([listing.lat, listing.lon])
      .bindPopup("<h2><a href=" + listing.url + " target='_blank'>" + listing.title + "</a></h2>" +
        "<h3>" + listing.company + "</h3>" +
        "<h3>" + listing.location + "</h3>" +
        "<h3>" + listing.salary + "</h3>" +
        "<h3>" + cleanOffice(listing.office) + "</h3>")
      .on("popupopen", function () {
        gsap.from(this._popup._container, { scale: 0, duration: 4 });
      });

    markers.addLayer(clusterMarker);

    // Create a listing marker for all job listings
    let listingMarker = L.marker([listing.lat, listing.lon])
      .bindPopup("<h2><a href=" + listing.url + " target='_blank'>" + listing.title + "</a></h2>" +
        "<h3>" + listing.company + "</h3>" +
        "<h3>" + listing.location + "</h3>" +
        "<h3>" + listing.salary + "</h3>" +
        "<h3>" + cleanOffice(listing.office) + "</h3>")
      .on("popupopen", function () {
        gsap.from(this._popup._container, { scale: 0, duration: 4 });
      });

    listingMarker.addTo(jobData);

    // Create a listing marker for in-person job listings
    if (listing.office === 'in_person') {
      let inPersonMarker = L.marker([listing.lat, listing.lon])
        .bindPopup("<h2><a href=" + listing.url + " target='_blank'>" + listing.title + "</a></h2>" +
          "<h3>" + listing.company + "</h3>" +
          "<h3>" + listing.location + "</h3>" +
          "<h3>" + listing.salary + "</h3>" +
          "<h3>" + cleanOffice(listing.office) + "</h3>")
        .on("popupopen", function () {
          gsap.from(this._popup._container, { scale: 0, duration: 4 });
        });

      inPersonMarker.addTo(inPerson);
    }

    // Create a listing marker for hybrid job listings
    if (listing.office === 'hybrid') {
      let hybridMarker = L.marker([listing.lat, listing.lon])
        .bindPopup("<h2><a href=" + listing.url + " target='_blank'>" + listing.title + "</a></h2>" +
          "<h3>" + listing.company + "</h3>" +
          "<h3>" + listing.location + "</h3>" +
          "<h3>" + listing.salary + "</h3>" +
          "<h3>" + cleanOffice(listing.office) + "</h3>")
        .on("popupopen", function () {
          gsap.from(this._popup._container, { scale: 0, duration: 4 });
        });

      hybridMarker.addTo(hybrid);
    }

    // Create a listing marker for remote job listings
    if (listing.office === 'remote') {
      let remoteMarker = L.marker([listing.lat, listing.lon])
        .bindPopup("<h2><a href=" + listing.url + " target='_blank'>" + listing.title + "</a></h2>" +
          "<h3>" + listing.company + "</h3>" +
          "<h3>" + listing.location + "</h3>" +
          "<h3>" + listing.salary + "</h3>" +
          "<h3>" + cleanOffice(listing.office) + "</h3>")
        .on("popupopen", function () {
          gsap.from(this._popup._container, { scale: 0, duration: 4 });
        });

      remoteMarker.addTo(remote);
    }
  }

  let uniqueStates = [...new Set(states)];

  function populateDropdown(statesArray) {
    let dropdown = document.getElementById("state-select");
    statesArray.forEach(function (state) {
      let option = document.createElement("option");
      option.value = state;
      option.textContent = state;
      dropdown.appendChild(option);
    });
  }

  populateDropdown(uniqueStates);

  function filterMarkers(selectedState) {
    markers.clearLayers();
    data.forEach(function (listing) {
      if (selectedState === "All" || listing.location === selectedState) {
        let clusterMarker = L.marker([listing.lat, listing.lon])
          .bindPopup("<h2><a href=" + listing.url + " target='_blank'>" + listing.title + "</a></h2>" +
            "<h3>" + listing.company + "</h3>" +
            "<h3>" + listing.location + "</h3>" +
            "<h3>" + listing.salary + "</h3>" +
            "<h3>" + cleanOffice(listing.office) + "</h3>")
          .on("popupopen", function () {
            gsap.from(this._popup._container, { scale: 0, duration: 4 });
          });
        markers.addLayer(clusterMarker);
      }
    });
  }

  let dropdown = document.getElementById("state-select");
  dropdown.addEventListener("change", function () {
    let selectedState = dropdown.value;
    if (selectedState === "All") {
      markers.addLayers(jobData.getLayers());
    } else {
      filterMarkers(selectedState);
    }
  });
});

// Overlay choice between cluster markers and all individual job listings
let overlayMaps = {
  "All Listings": jobData,
  "Cluster Map": markers,
  "In Person": inPerson,
  "Hybrid": hybrid,
  "Remote": remote
};

// Pass our map layers into our layer control.
// Add the layer control to the map.
L.control.layers(null, overlayMaps).addTo(myMap);















