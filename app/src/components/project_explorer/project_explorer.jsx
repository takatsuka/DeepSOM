
import * as React from 'react'
import { Component } from 'react';

import { Classes, Icon, Intent, TreeNodeInfo, Tree, Elevation, Card, Button, ButtonGroup } from "@blueprintjs/core";
import { Classes as Popover2Classes, ContextMenu2, Tooltip2 } from "@blueprintjs/popover2";
import DragDropSOM from '../drag-drop/drag-drop';
import ImageView from '../imageview/imageview';
import ScatterView3D from '../scatterview_3d/scatterview';

class ProjectExplorer extends Component {
    constructor(props) {
        super(props)

        var treeContent = [
            {
                id: 0,
                hasCaret: true,
                icon: "folder-close",
                label: "Data",
            },

            {
                id: 143,
                hasCaret: false,
                isExpanded: true,
                icon: "graph",
                label: "deepsom",
                
            },

            {
                id: 22,
                hasCaret: false,
                isExpanded: false,
                icon: "graph",
                label: "not_so_deepsom",
            },
            {
                id: 3,
                hasCaret: true,
                isExpanded: false,
                icon: "folder-close",
                label: "Vis",
                childNodes: [
                    {
                        id: 98,
                        icon: "heatmap",
                        label: "sphere_viz",

                    },
                    {
                        id: 111,
                        icon: "heatmap",
                        label: "donut_viz",

                    },

                    {
                        id: 96,
                        icon: "media",
                        label: "fashion_imgset",

                    },
                ]
            },
        ]

        this.state = {
            tree: treeContent
        }
    }

    componentDidMount() {

    }

    updateTree(thing){
        thing()
        this.setState({tree: this.state.tree})
    }

    handleOpen(id){
        if(id == 143) {
            this.props.openTab(<DragDropSOM />, "deepsom", true, "/Volumes/Sweep\ SSD/comp3988pre/dsom.json")
        }

        if(id == 22) {
            this.props.openTab(<DragDropSOM />, "not_so_deepsom", true, "/Volumes/Sweep\ SSD/comp3988pre/som.json")
        }

        if(id == 96) {
            this.props.openTab(<ImageView />, "fashion_imgset", true, "load")
        }

        if(id == 98) {
            this.props.openTab(<ScatterView3D />, "sphere_viz", true, {d: "/Volumes/Sweep\ SSD/comp3988pre/sphere_64.txt", t: "/Volumes/Sweep\ SSD/comp3988pre/sphere.json"})
        }

        if(id == 111) {
            this.props.openTab(<ScatterView3D />, "donut_viz", true, {d: "/Volumes/Sweep\ SSD/comp3988pre/donut_512.txt", t: "/Volumes/Sweep\ SSD/comp3988pre/donut.json"})
        }
    }

    render() {

        return (
            <>
                <ButtonGroup minimal={false} elevation={Elevation.FOUR} fill={true} alignText="left" minimal={true} large={true}>
                    <Button active={true} >pres-demo-2</Button>

                </ButtonGroup>

                <Tree elevation={Elevation.FOUR}
                    onNodeExpand={(x) => (this.updateTree(() => x.isExpanded = true))}
                    onNodeCollapse={(x) => (this.updateTree(() => x.isExpanded = false))}
                    onNodeClick={(x) => this.handleOpen(x.id)}
                    contents={this.state.tree}

                />


            </>)

    }
}

export default ProjectExplorer;
