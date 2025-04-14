// amCharts Globe Script
// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

var chart = am4core.create("chartdiv", am4maps.MapChart);

// Disable amCharts logo
chart.logo.disabled = true;

// Set map definition
chart.geodata = am4geodata_worldLow;

// Set projection
chart.projection = new am4maps.projections.Orthographic();
chart.panBehavior = "rotateLongLat";
chart.deltaLatitude = -20;
chart.padding(20, 20, 20, 20);

// Create map polygon series
var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());

// Make map load polygon data from GeoJSON
polygonSeries.useGeodata = true;

// Configure series
var polygonTemplate = polygonSeries.mapPolygons.template;
polygonTemplate.fill = am4core.color("#228B22"); // Green for land
polygonTemplate.stroke = am4core.color("#000080"); // Navy blue for outlines
polygonTemplate.strokeWidth = 0.5;

// Remove country names and internal state outlines
polygonTemplate.tooltipText = ""; // No country names
polygonSeries.exclude = ["AQ"]; // Exclude Antarctica for a cleaner look

// Add ocean background
chart.backgroundSeries.mapPolygons.template.polygon.fill = am4core.color("#87CEEB"); // Light blue for oceans
chart.backgroundSeries.mapPolygons.template.polygon.fillOpacity = 1;

// Add data for stats
var imageSeries = chart.series.push(new am4maps.MapImageSeries());
var imageTemplate = imageSeries.mapImages.template;
imageTemplate.propertyFields.latitude = "latitude";
imageTemplate.propertyFields.longitude = "longitude";
imageTemplate.tooltipText = "{stat}: {value}";
imageTemplate.nonScaling = true;

// Add animated flag to dots
var flag = imageTemplate.createChild(am4core.Image);
flag.href = "https://cdn-icons-png.flaticon.com/512/197/197560.png"; // Example flag icon
flag.width = 60; // 3x larger than before
flag.height = 60; // 3x larger than before
flag.horizontalCenter = "middle";
flag.verticalCenter = "bottom";
flag.dy = -20; // Position above the circle
flag.tooltipText = "{stat}: {value}";
flag.propertyFields.href = "flag"; // Dynamic flag image

var circle = imageTemplate.createChild(am4core.Circle);
circle.radius = 6;
circle.fill = am4core.color("#FFD700"); // Gold color for foodie theme
circle.stroke = am4core.color("#FFFFFF");
circle.strokeWidth = 2;

// Add data points
imageSeries.data = [
    { latitude: 35.6895, longitude: 139.6917, stat: "Spiciness", value: "9/10", flag: "https://cdn-icons-png.flaticon.com/512/197/197604.png" }, // Tokyo
    { latitude: 48.8566, longitude: 2.3522, stat: "Plating", value: "8/10", flag: "https://cdn-icons-png.flaticon.com/512/197/197560.png" }, // Paris
    { latitude: 40.7128, longitude: -74.0060, stat: "Deliciousness", value: "7/10", flag: "https://cdn-icons-png.flaticon.com/512/197/197484.png" }, // New York
    { latitude: -33.8688, longitude: 151.2093, stat: "Value", value: "6/10", flag: "https://cdn-icons-png.flaticon.com/512/197/197507.png" } // Sydney
];

// Rotate globe animation
let animation = chart.animate({ property: "deltaLongitude", to: 100000 }, 20000000);

// Stop animation on user interaction and resume from the new position
chart.seriesContainer.events.on("down", function () {
    if (animation) {
        animation.stop();
    }
});

chart.seriesContainer.events.on("up", function () {
    // Resume rotation from the current position
    animation = chart.animate({ property: "deltaLongitude", to: 100000 }, 20000000);
});
