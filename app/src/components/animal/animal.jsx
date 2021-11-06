import * as React from 'react';
import { Component } from 'react';
import "./animal.scss";

import { Switch, Button, ButtonGroup } from "@blueprintjs/core";

import bear from '../../../imgs/animal/__bear.png';
import bird from '../../../imgs/animal/__bird.png';
import bull from '../../../imgs/animal/__bull.png';
import cat from '../../../imgs/animal/__cat.png';
import chicken from '../../../imgs/animal/__chicken.png';
import cow from '../../../imgs/animal/__cow.png';
import dog from '../../../imgs/animal/__dog.png';
import duck from '../../../imgs/animal/__duck.png';
import elephant from '../../../imgs/animal/__elephant.png';
import floppy_eared_dog from '../../../imgs/animal/__floppy-eared-dog.png';
import gorilla from '../../../imgs/animal/__gorilla.png';
import hen from '../../../imgs/animal/__hen.png';
import hippo from '../../../imgs/animal/__hippo.png';
import octopus from '../../../imgs/animal/__octopus.png';
import pig from '../../../imgs/animal/__pig.png';
import rhino from '../../../imgs/animal/__rhino.png';
import shark from '../../../imgs/animal/__shark.png';
import textured_cat from '../../../imgs/animal/__textured-cat.png';
import turtle from '../../../imgs/animal/__Turtle.png';
import whale from '../../../imgs/animal/__whale.png';

class AnimalTile extends Component {
    constructor(props) {
        super(props);
        this.size = 200;
    }

    render() {
        let tiles = [];
        for (var i = 0; i < this.props.data.length; i++) {
            let row = [];
            for (var j = 0; j < this.props.data[i].length; j++) {
                if (this.props.data[i][j] == null) {
                    row.push(<div className="tile"></div>);
                } else {
                    let cell = [];

                    for (var k = 0; k < this.props.data[i][j].length; k++) {
                        cell.push(<div className="animal-icon"><img src={this.props.data[i][j][k]}/></div>);
                    }

                    if (this.props.data[i][j].length <= 4) {
                        row.push(<div className="tile"><div className="animal-box">{cell}</div></div>);
                    } else {
                        // tight layout if animals > 4
                        row.push(<div className="tile"><div className="animal-box tight">{cell}</div></div>);
                    }
                }
            }
            tiles.push(<div className="animal-row">{row}</div>);
        }
        return <div className="platform">
                  {tiles}
            </div>;
    }
}

class Animal extends Component {
    constructor(props) {
        super(props);
        this.shark = this.shark.bind(this);
        this.projection_toggle = this.projection_toggle.bind(this);
        this.state = {
            data: [
                [[bear], [elephant], [chicken], null],
                [[bird], [bull, gorilla, pig, bull, gorilla, pig, bull, gorilla, pig], [cat], null],
                [[turtle], [hen, hippo, elephant, duck, dog, pig], [hippo, elephant, duck, dog], null],
                [null, null, null, null],
            ],
            iter: 0,
            isometric: true,
        };
        this.sharkindex = [
            [3, 0],
            [3, 1],
            [3, 2],
            [3, 3],
            [2, 3],
            [1, 3],
            [0, 3],
            [0, 2],
            [0, 1],
            [0, 0],
            [1, 0],
            [2, 0]
        ];

    }

    shark() {
        var that = this;
        setTimeout(function() {

            var iter = that.state.iter;
            var idx = that.sharkindex[iter];
            that.state.data[idx[0]][idx[1]] = null;

            iter++;
            iter %= that.sharkindex.length;

            idx = that.sharkindex[iter];
            that.state.data[idx[0]][idx[1]] = [shark];

            that.setState({
                iter: iter,
                data: that.state.data
            });

            that.shark();
        }, 150)
    }

    projection_toggle() {
        if (this.state.isometric) {
            document.getElementById('animal-viz').classList.remove('isometric');
        } else {
            document.getElementById('animal-viz').classList.add('isometric');
        }
        this.setState(prevState => ({isometric: !prevState.isometric}));
    }

    render() {
        return <div>
            <div className="submenu">
                <ButtonGroup style={{ minWidth: 200 }} minimal={true} className="sm-buttong">
                    <Button className="bp3-minimal" icon="presentation" text="Baby Shark Mode" onClick={this.shark}/>
                    <Switch style={{marginLeft:"10px", marginTop:"5px"}} large checked={this.state.isometric} innerLabel="Planar" innerLabelChecked="Isometric" onChange={this.projection_toggle} />
                </ButtonGroup>
            </div>

            <div className="animal-viz-container isometric" id="animal-viz">
                <AnimalTile data={this.state.data}/>
            </div>

        </div>;
    }
}

export default Animal;
