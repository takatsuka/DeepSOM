
import * as React from 'react'
import { Component } from 'react';

import { Classes, Icon, Intent, TreeNodeInfo, Tree, Elevation, Card, Button, ButtonGroup } from "@blueprintjs/core";
import { Classes as Popover2Classes, ContextMenu2, Tooltip2 } from "@blueprintjs/popover2";


class ProjectExplorer extends Component {
    constructor(props) {
        super(props)
        this.state = {

        }
    }

    componentDidMount() {

    }


    render() {

        return (
            <>
                <ButtonGroup minimal={false} elevation={Elevation.FOUR} fill={true} alignText="left" minimal={true} large={true}>
                    <Button active={true} >untitled project</Button>
                    
                </ButtonGroup>

                <Tree elevation={Elevation.FOUR}
                    contents={[
                        {
                            id: 0,
                            hasCaret: true,
                            icon: "folder-close",
                            label: "Data",
                        },

                        {
                            id: 1,
                            hasCaret: true,
                            isExpanded: true,
                            icon: "graph",
                            label: "deepsom",
                            childNodes: [
                                {
                                    id: 2,
                                    icon: "regression-chart",
                                    label: "LVQ",
                                },
                                {
                                    id: 3,
                                    icon: "layout-grid",
                                    label: "top_som",
                                },
                                {
                                    id: 4,
                                    icon: "many-to-one",
                                    label: "sampler2",
                                    hasCaret: true,
                                },
                            ]
                        },

                        {
                            id: 2,
                            hasCaret: true,
                            isExpanded: false,
                            icon: "graph",
                            label: "not_so_deepsom",
                            childNodes: [
                                {
                                    id: 4,
                                    icon: "regression-chart",
                                    label: "LVQ",
                                },
                                {
                                    id: 5,
                                    icon: "layout-grid",
                                    label: "top_som",
                                },
                                {
                                    id: 7,
                                    icon: "many-to-one",
                                    label: "sampler2",
                                    hasCaret: true,
                                },
                            ]
                        },

                        {
                            id: 3,
                            hasCaret: false,
                            isExpanded: false,
                            icon: "heatmap",
                            label: "sphere_viz",

                        },

                        {
                            id: 4,
                            hasCaret: false,
                            isExpanded: false,
                            icon: "heatmap",
                            label: "donut_viz",

                        },
                    ]}

                />


            </>)

    }
}

export default ProjectExplorer;
