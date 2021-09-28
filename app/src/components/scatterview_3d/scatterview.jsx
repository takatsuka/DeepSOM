
import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuItem, Position, Button, ButtonGroup, Tab, Tabs, Intent, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay } from "@blueprintjs/core";
import "./scatterview.scss"

const d3 = require("d3");
import { _3d } from 'd3-3d';


class ScatterView3D extends Component {
    constructor(props) {
        super(props)

        this.initView = this.initView.bind(this)
        this.d3view = React.createRef()

        this.state = {

        }
    }

    componentDidMount() {
        this.initView()
    }

    // Predefined function to return x coordinate for drawing purposes
    posPointX(d) {
        return d.projected.x;
    }

    // Predefined function to return y coordinate for drawing purposes
    posPointY(d) {
        return d.projected.y;
    }

    // Draws scatter points with inputted coordinate data
    drawPoints(data, tt) {
        const svg = this.svg
        const cm = this.colorMap
        console.log(this)
        var points = svg.selectAll('circle').data(data, (d) => { d.id });
        points
            .enter()
            .append('circle')
            .attr('class', '_3d')
            .attr('opacity', 0)
            .attr('cx', this.posPointX)
            .attr('cy', this.posPointY)
            .merge(points)
            .transition().duration(tt)
            .attr('r', 3)
            .attr('stroke', (d) => d3.color(cm(d.id)).darker(3))
            .attr('fill', (d) => d3.color(cm(d.id)))
            .attr('opacity', 1)
            .attr('cx', this.posPointX)
            .attr('cy', this.posPointY);

        points.exit().remove();
    }

    // Draws axis scale and text
    drawAxis(data, axis, _3dObject) {
        const svg = this.svg
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
            .each(function (d) {
                d.centroid = { x: d.rotated.x, y: d.rotated.y, z: d.rotated.z };
            })
            .attr('x', this.posPointX)
            .attr('y', this.posPointY)
            .text(function (d) { return d[dimension]; });

        text.exit().remove();
    }


    // Function to run when file is successfully loaded and contents are read in
    // TODO: this function is kept for to remaind compatible, might be removed since load was done in python
    loadData(data) {
        var scatter = [], xLine = [], yLine = [], zLine = [];
        var counter = 0; // For assigning point IDs



        // Iterate through each line of data
        for (let i = 0; i < data.length; i++) {
            let tokens = data[i];
            let pointX = parseFloat(tokens[0]);
            let pointY = parseFloat(tokens[1]);
            let pointZ = parseFloat(tokens[2]);
            // Append float data to list
            scatter.push({ x: pointX, y: pointY, z: pointZ, id: 'point_' + counter++ });
        }

        // Define values for xyz scales
        for (let i = -1; i <= 1; i = i + 0.5) {
            xLine.push([-i, 1, -1]);
            yLine.push([-1, i, -1]);
            zLine.push([-1, 1, -i]);
        }

        // Input data for d3 drawing
        var result = [
            scatter,
            [xLine],
            [yLine],
            [zLine]
        ];

        return result;
    }

    initView() {
        const svg = d3.select(this.d3view.current)
        this.svg = svg
        this.colorMap = d3.scaleOrdinal(d3.schemeCategory10);
        const rawData = this.loadData(this.props.data) // TODO: 



        var mx, my, mouseX, mouseY;
        var dataCoordinates, weightsCoordinates;

        /* -------- d3 object configurations -------- */
        let origin = [480, 300], j = 1, scale = 200, scatter = [], xLine = [], yLine = [], zLine = [], beta = 0, alpha = 0, key = function (d) { return d.id; }, startAngle = Math.PI / 4;


        /* -------- d3 object initialisations -------- */
        // Points
        let point3d = _3d()
            .x(function (d) { return d.x; })
            .y(function (d) { return d.y; })
            .z(function (d) { return d.z; })
            .origin(origin)
            .rotateY(startAngle)
            .rotateX(-startAngle)
            .scale(scale);

        // X axis
        let xScale3d = _3d()
            .shape('LINE_STRIP')
            .origin(origin)
            .rotateY(startAngle)
            .rotateX(-startAngle)
            .scale(scale);

        // Y axis
        let yScale3d = _3d()
            .shape('LINE_STRIP')
            .origin(origin)
            .rotateY(startAngle)
            .rotateX(-startAngle)
            .scale(scale);

        // Z axis
        let zScale3d = _3d()
            .shape('LINE_STRIP')
            .origin(origin)
            .rotateY(startAngle)
            .rotateX(-startAngle)
            .scale(scale);

        let currentCoordinates = [
            point3d(rawData[0]),
            xScale3d(rawData[1]),
            yScale3d(rawData[2]),
            zScale3d(rawData[3]),
        ];

        this.drawPoints(currentCoordinates[0], 1);
        this.drawAxis(currentCoordinates[1], 'x', xScale3d);
        this.drawAxis(currentCoordinates[2], 'y', yScale3d);
        this.drawAxis(currentCoordinates[3], 'z', zScale3d);
    }

    embedCard(whatever) {
        return (
            <Card interactive={false} elevation={Elevation.TWO}>
                {whatever}
            </Card>
        )
    }

    render() {


        return (
            <>
                <svg className="svg-render" ref={this.d3view} />
            </>)

    }
}

export default ScatterView3D;
