// Function to draw or redraw scatter plot with the given data
function drawPlot(data, tt){
    drawPoints(data[0], tt);
    drawAxis(data[1], 'x', xScale3d);
    drawAxis(data[2], 'y', yScale3d);
    drawAxis(data[3], 'z', zScale3d);
}

function updatePlot() {
    let result = [
        point3d(currentCoordinates[0]),
        xScale3d(currentCoordinates[1]),
        yScale3d(currentCoordinates[2]),
        zScale3d(currentCoordinates[3]),
    ];
    drawPlot(result, 1000);
}

// Draws scatter points with inputted coordinate data
function drawPoints(data, tt) {
    var points = svg.selectAll('circle').data(data, key);
    points
        .enter()
        .append('circle')
        .attr('class', '_3d')
        .attr('opacity', 0)
        .attr('cx', posPointX)
        .attr('cy', posPointY)
        .merge(points)
        .transition().duration(tt)
        .attr('r', 3)
        .attr('stroke', function(d){ return d3.color(color(d.id)).darker(3); })
        .attr('fill', function(d){ return color(d.id); })
        .attr('opacity', 1)
        .attr('cx', posPointX)
        .attr('cy', posPointY);

    points.exit().remove();
}

// Draws axis scale and text
function drawAxis(data, axis, _3dObject) {
    // Draw scale
    let scale = svg.selectAll('path.' + axis + "Scale").data(data);
    scale
        .enter()
        .append('path')
        .attr('class', '_3d ' + axis + "Scale")
        .merge(scale)
        .attr('stroke', 'black')
        .attr('stroke-width', .5)
        .attr('d', _3dObject.draw);

    scale.exit().remove();

    // Determine dimension to read from and write to
    let dimension = 0;
    switch (axis) {
        case "x":
            dimension = 0;
            break;
        case "y":
            dimension = 1;
            break;
        case "z":
            dimension = 2;
            break;
        default:
            break;
    }

    // Write scale text
    let text = svg.selectAll('text.' + axis + 'Text').data(data[0]);
    text
        .enter()
        .append('text')
        .attr('class', '_3d ' + axis + 'Text')
        .attr('dx', '.3em')
        .merge(text)
        .each(function(d){
            d.centroid = {x: d.rotated.x, y: d.rotated.y, z: d.rotated.z};
        })
        .attr('x', posPointX )
        .attr('y', posPointY )
        .text(function(d){ return d[dimension]; });

    text.exit().remove();
}

// Predefined function to return x coordinate for drawing purposes
function posPointX(d){
    return d.projected.x;
}

// Predefined function to return y coordinate for drawing purposes
function posPointY(d){
    return d.projected.y;
}