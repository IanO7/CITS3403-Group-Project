am4core.useTheme(am4themes_animated);

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
polygonSeries.useGeodata = true;

// Configure series
var polygonTemplate = polygonSeries.mapPolygons.template;
polygonTemplate.fill = am4core.color("#228B22");
polygonTemplate.stroke = am4core.color("#000080");
polygonTemplate.strokeWidth = 0.5;

// Exclude Antarctica
polygonSeries.exclude = ["AQ"];

// Add ocean background
chart.backgroundSeries.mapPolygons.template.polygon.fill = am4core.color("#87CEEB");
chart.backgroundSeries.mapPolygons.template.polygon.fillOpacity = 1;

// Add data for stats
var imageSeries = chart.series.push(new am4maps.MapImageSeries());
var imageTemplate = imageSeries.mapImages.template;
imageTemplate.propertyFields.latitude = "latitude";
imageTemplate.propertyFields.longitude = "longitude";
imageTemplate.tooltipHTML = `
    <div style="text-align: center;">
        <img src="{flag}" alt="Flag" style="width: 50px; height: 30px; margin-bottom: 5px;">
        <div>{stat}: {value}</div>
    </div>
`;
imageTemplate.nonScaling = true;

// Add circular flag images
var flagImage = imageTemplate.createChild(am4core.Image);
flagImage.propertyFields.href = "flag";
flagImage.width = 30;
flagImage.height = 30;
flagImage.horizontalCenter = "middle";
flagImage.verticalCenter = "middle";
flagImage.circle = true; // Make the image circular
flagImage.stroke = am4core.color("#FFFFFF");
flagImage.strokeWidth = 2;

// Add data points
imageSeries.data = [
    { latitude: 35.6895, longitude: 139.6917, stat: "Spiciness", value: "9/10", flag: "https://cdn-icons-png.flaticon.com/512/197/197604.png" }, // Tokyo
    { latitude: 48.8566, longitude: 2.3522, stat: "Service", value: "8/10", flag: "https://cdn-icons-png.flaticon.com/512/197/197560.png" }, // Paris
    { latitude: 40.7128, longitude: -74.0060, stat: "Deliciousness", value: "7/10", flag: "https://cdn-icons-png.flaticon.com/512/197/197484.png" }, // New York
    { latitude: -33.8688, longitude: 151.2093, stat: "Value", value: "6/10", flag: "https://cdn-icons-png.flaticon.com/512/197/197507.png" }, // Sydney
    { latitude: 55.7558, longitude: 37.6173, stat: "Uniqueness", value: "8/10", flag: "https://cdn-icons-png.flaticon.com/512/197/197408.png" } // Moscow
];

// Rotate globe animation
let animation = chart.animate({ property: "deltaLongitude", to: 100000 }, 20000000);

chart.seriesContainer.events.on("down", function () {
    if (animation) {
        animation.stop();
    }
});

chart.seriesContainer.events.on("up", function () {
    animation = chart.animate({ property: "deltaLongitude", to: 100000 }, 20000000);
});