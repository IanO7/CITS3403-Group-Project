// Apply animated theme
am4core.useTheme(am4themes_animated);

var chart = am4core.create("chartdiv", am4maps.MapChart);

// Disable amCharts credit link
chart.logo.disabled = true;

// World map & orthographic projection
chart.geodata = am4geodata_worldLow;
chart.projection = new am4maps.projections.Orthographic();
chart.panBehavior = "rotateLongLat";
chart.deltaLatitude = -20;
chart.padding(20, 20, 20, 20);

// Country polygons
var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
polygonSeries.useGeodata = true;
polygonSeries.exclude = ["AQ"];  // no Antarctica

var polyTemplate = polygonSeries.mapPolygons.template;
polyTemplate.fill = am4core.color("#228B22");
polyTemplate.stroke = am4core.color("#000080");
polyTemplate.strokeWidth = 0.5;

// Ocean background
chart.backgroundSeries.mapPolygons.template.polygon.fill = am4core.color("#87CEEB");
chart.backgroundSeries.mapPolygons.template.polygon.fillOpacity = 1;

// Image (pin) series
var imageSeries = chart.series.push(new am4maps.MapImageSeries());
var imageTemplate = imageSeries.mapImages.template;

// 1) Bind latitude & longitude
imageTemplate.propertyFields.latitude  = "latitude";
imageTemplate.propertyFields.longitude = "longitude";

// 2) Use custom HTML tooltip that shows the fetched image + text
imageTemplate.tooltipHTML = `
  <div style="text-align: center; max-width: 150px;">
    <img src="{url}" alt="Pin image" style="width: 50px; height: 30px; margin-bottom: 5px; border-radius: 3px;">
    <div style="font-weight: bold; margin-bottom: 4px;">{title}</div>
    <div style="font-size: 0.9em;">{tooltip}</div>
  </div>
`;
imageTemplate.nonScaling = true;

// 3) Add the flag/image element, binding its href to your `url` field
var flagImage = imageTemplate.createChild(am4core.Image);
flagImage.propertyFields.href = "url";
flagImage.width  = 30;
flagImage.height = 30;
flagImage.horizontalCenter = "middle";
flagImage.verticalCenter   = "middle";
flagImage.circle           = true;
flagImage.stroke           = am4core.color("#FFFFFF");
flagImage.strokeWidth      = 2;

// 4) Fetch your live data and map it into the series
fetch(window.GLOBE_API_URL)
  .then(r => r.json())
  .then(data => {
    imageSeries.data = data.map(d => ({
      latitude:  d.lat,
      longitude: d.lng,
      title:     d.title,
      tooltip:   d.tooltip,
      url:       d.imageUrl
    }));
    // redraw with new data
    chart.invalidateRawData();
  })
  .catch(err => console.error("Failed to load globe pins:", err));

// 5) Continuous rotation, pausing on user drag
let animation = chart.animate({ property: "deltaLongitude", to: 100000 }, 20000000);

chart.seriesContainer.events.on("down", () => {
  if (animation) {
    animation.stop();
  }
});

chart.seriesContainer.events.on("up", () => {
  animation = chart.animate({ property: "deltaLongitude", to: 100000 }, 20000000);
});
