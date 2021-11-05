import * as React from 'react';
import { Component } from 'react';
import "./animal.scss";

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
            for (var j = 0; j < this.props.data[i].length; j++) {
                if (this.props.data[i][j] == null) {
                    tiles.push(<div class="tile"></div>);
                } else {
                    tiles.push(<div class="tile"><div class="animal-box"><img src={this.props.data[i][j]} class="animal-icon"/></div></div>);
                }
            }
        }
        return <div class="animal-viz-container">
                        <img src={bear}/>
                  <label for="ossm">Rotation</label>
                  <input type="checkbox" id="ossm" name="ossm"/>
                  <div class="platform">
                  {tiles}
                  </div>
                </div>;
    }
}

class Animal extends Component {
    constructor(props) {
        super(props);
        this.shark = this.shark.bind(this);
        this.state = {
            data: [
                [bear, elephant, chicken, null],
                [bird, bull, cat, null],
                [turtle, pig, hippo, null],
                [null, null, null, null]
            ],
            iter: 0
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
            that.state.data[idx[0]][idx[1]] = shark;

            that.setState({
                iter: iter,
                data: that.state.data
            });

            that.shark();
        }, 150)
    }

    render() {
        return <div>
        <button onClick={this.shark}>Baby shark</button>

        <AnimalTile data={this.state.data}/>

        </div>;
    }
}

export default Animal;
