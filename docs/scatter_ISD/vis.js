// Set the dimensions of the chart
var width = 650;
var height = 450;
// Set the margins of the chart
var margin = {
  top: 20,
  right: 20,
  bottom: 50,
  left: 120
};

// retreive json data
const url = 'https://s3.amazonaws.com/interactives.dallasnews.com/jobtests/graphicsreporter/testdata.json';
const response = fetch(url)
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();
  });

// call function and visualize data
response.then(function (json) {
  update_json(json);
  visualize(json.data)
});

// function to aggregate enrollment, calculate average enrollment 
// and number of schools for each ISD
function update_json(json) {
  Object.keys(json.data).forEach(isd_record => {
    Object.keys(json.data[isd_record]).forEach(key => {
      if (key == "data") {
        let enrollment = 0;
        let num_schools = 0;

        Object.keys(json.data[isd_record]["data"]).forEach(entry => {
          school_record = json.data[isd_record]["data"][entry];
          enrollment += school_record["enrollment"];
          num_schools += 1;
        })
        
        json.data[isd_record]["total_enrollment"] = enrollment;
        json.data[isd_record]["avg_enrollment"] = parseInt(enrollment / num_schools);
        json.data[isd_record]["num_schools"] = num_schools;
      }
    })
  })
};

// function to visualize data
function visualize(data) {
  // append SVG element to <div>
  let svg = d3.select("#chart-1")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // create axis variables
  let x = d3.scaleLinear().range([0, (width - margin.left - margin.right)])
    .domain([0, d3.max(data, d => +d.total_enrollment)]);
    //.domain(d3.extent(data, d => +d.total_enrollment));

  let y = d3.scaleLinear().range([(height - margin.top - margin.bottom), 0])
    .domain([40000, d3.max(data, d => +d.mhi)]);
    //.domain(d3.extent(data, d => +d.mhi));

  // append X-axis
  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + y.range()[0] + ")") // controls horizontal position of the Axis
    .call(d3.axisBottom(x));

  // append Y-axis
  svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(-15,0)")   // controls vertical position of the Axis
    .call(d3.axisLeft(y));

  // append X-axis label
  svg.append("text")
    .attr("text-anchor", "end")
    .style("font-size", "16px")
    .style("font-family", "system-ui")
    .attr("x", margin.right + 480)
    .attr("y", margin.top + 400)
    .text("Total district enrollment");

  // append Y-axis label
  svg.append("text")
    .attr("text-anchor", "end")
    .style("font-size", "16px")
    .attr("transform", "rotate(-90)")
    .attr("y", -margin.left + 45)
    .attr("x", -margin.top)
    .text("Median household income($)");

  // create a tooltip variable
  let tooltip = d3.select("#chart-1")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "wheat")
    .style("border", "solid")
    .style("border-width", "1px")
    .style("border-radius", "5px")
    .style("padding", "5px");

  // function to update display when user hovers over the circle
  let mouseover = function (d) {
    // highlight circle when user hovers over the circle
    d3.select(this)
      .style("fill", "wheat")
      .style("stroke", "cornflowerblue")
      .style("stroke-width", 1.5)
      .style("opacity", 1)
      .attr("tooltip");
    // display values in the tooltip when user hovers over the circle
    tooltip.html(d["NAME"] + "<br/> Number of schools: " + d["num_schools"] + "<br/> Average enrollment: " + d["avg_enrollment"] + "<br/> UIL totals: " + d["UIL totals"])
      .style("opacity", 0.9)
      .style("left", (event.pageX) + "px")
      .style("top", (event.pageY) + "px");
  }

  // function to update the tooltip when user leaves the circle
  let mouseleave = function (d) {
    d3.select(this)
      .style("stroke", "white")
      .style("fill", "cornflowerblue")
      .style("opacity", 0.7);
    tooltip.style("opacity", 0);
  }

  // append circles to the chart
  const radiusScale = d3.scaleSqrt()
    .domain([0, 100])
    .range([0, 10]);

  svg.selectAll("circle")
    .data(data)
    .enter()
    .append("circle")
    .attr("cx", d => x(+d["total_enrollment"]))
    .attr("cy", d => y(+d["mhi"]))
    .attr("r", d => radiusScale(+d["UIL totals"] + 1) * 4)
    .style("fill", "cornflowerblue")
    .style("opacity", 0.7)
    .style("stroke", "white")
    .style("stroke-width", "1px")
    .on("mouseover", mouseover)
    .on("mouseleave", mouseleave);
}
