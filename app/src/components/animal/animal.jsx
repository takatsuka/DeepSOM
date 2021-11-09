import * as React from 'react';
import { Component } from 'react';
import "./animal.scss";

import { Switch, Button, ButtonGroup, Intent } from "@blueprintjs/core";
import { PrimaryToaster } from '../common/toaster';
import bear from './imgs/__bear.png';
import bird from './imgs/__bird.png';
import bull from './imgs/__bull.png';
import cat from './imgs/__cat.png';
import chicken from './imgs/__chicken.png';
import cow from './imgs/__cow.png';
import dog from './imgs/__dog.png';
import duck from './imgs/__duck.png';
import elephant from './imgs/__elephant.png';
import floppy_eared_dog from './imgs/__floppy-eared-dog.png';
import gorilla from './imgs/__gorilla.png';
import hen from './imgs/__hen.png';
import hippo from './imgs/__hippo.png';
import octopus from './imgs/__octopus.png';
import pig from './imgs/__pig.png';
import rhino from './imgs/__rhino.png';
import shark from './imgs/__shark.png';
import textured_cat from './imgs/__textured-cat.png';
import turtle from './imgs/__Turtle.png';
import whale from './imgs/__whale.png';

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
                        cell.push(<div className="animal-icon"><img src={this.props.data[i][j][k]} /></div>);
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
                [[], [], [], []],
            ],
            iter: 0,
            isometric: true,
            service: null,
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

        if (window.pywebview)
            window.pywebview.api.launch_service("AnimalService").then((x) => (
                this.setState({
                    service: x
                })
            ))

    }

    pickInput() {
        this.props.fileman.ask_user_pick_data("Select a SOM", "opaque", (k) => {
            window.pywebview.api.call_service(this.state.service, "set_input", [k]).then((e) => {

                if (!e.status) {
                    PrimaryToaster.show({
                        message: (e.status ? "SOM Opened." : "Failed: ") + e.msg,
                        intent: e.status ? Intent.SUCCESS : Intent.DANGER,
                    });
                }

                window.pywebview.api.call_service(this.state.service, "get_animal_data", []).then((e) => {
                    var animalMap = {
                        "Dove": bird,
                        "Chicken": chicken,
                        "Duck": duck,
                        "Goose": hen,
                        "Owl": cow,
                        "Hawk": cow,
                        "Eagle": cow,
                        "Fox": cow,
                        "Dog": dog,
                        "Wolf": hippo,
                        "Cat": cow,
                        "Tiger": cow,
                        "Lion": cow,
                        "Horse": cow,
                        "Zebra": cow,
                        "Cow": cow
                    }
                    var d = e.obj.map((e) => e.map((a) => a.map((q) => animalMap[q])))

                    this.setState({data: d}, () => {
                        
                    })
                });
            });
        })

    }

    shark() {
        var that = this;
        setTimeout(function () {

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
        this.setState(prevState => ({ isometric: !prevState.isometric }));
    }

    render() {
        return <div>
            <div className="submenu">
                <ButtonGroup style={{ minWidth: 200 }} minimal={true} className="sm-buttong">
                    <Button icon="document" onClick={() => this.pickInput()}>Select Model</Button>
                    <Button className="bp3-minimal" icon="presentation" text="Baby Shark Mode" onClick={this.shark} />
                    <Switch style={{ marginLeft: "10px", marginTop: "5px" }} large checked={this.state.isometric} innerLabel="Planar" innerLabelChecked="Isometric" onChange={this.projection_toggle} />
                </ButtonGroup>
            </div>

            <div className="animal-viz-container isometric" id="animal-viz">
                <AnimalTile data={this.state.data} />
            </div>

        </div>;
    }
}

export default Animal;
