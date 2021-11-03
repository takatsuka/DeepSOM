
import * as React from 'react'
import { Component } from 'react';

import { Classes, Icon, Intent, TreeNodeInfo, Tree, Elevation, Card, Button, ButtonGroup } from "@blueprintjs/core";
import { Classes as Popover2Classes, ContextMenu2, Tooltip2 } from "@blueprintjs/popover2";
import { TAG_INPUT_VALUES } from '@blueprintjs/core/lib/esm/common/classes';


class ProjectExplorer extends Component {
    constructor(props) {
        super(props)

        var treeContent = []

        this.state = {
            services: null,
            tree: treeContent,
            nModels: 0,
        }
    }

    componentDidMount() {

    }

    loadModel() {
        window.pywebview.api.call_service(this.props.datastore, "load_som_container", []).then((som) => {
            if (som != null) {
                let childNodes = []

                for (let i = 0; i < som.childNodes.length; i++) {
                    console.log(som.childNodes[i])
                    childNodes.push({
                        icon: "database",
                        label: som.childNodes[i],
                    })
                }

                let model = {
                    isExpanded: true,
                    icon: "folder-close",
                    label: som.label,
                    childNodes: childNodes
                }

                this.state.nModels++;
                this.state.tree.push(model);
                this.setState((state) => {
                    return { tree: state.tree }
                })
            }
        })
    }

    // The explorer works like a stack at the moment, this is the push operation
    // (TODO) Should be the SOM container that is selected by the user
    addNewModel() {
        window.pywebview.api.call_service(this.props.datastore, "create_som_container", ["SOM Model " + this.state.nModels]).then((descriptor) => {
            let newModel = {
                isExpanded: true,
                icon: "folder-close",
                label: descriptor,
                childNodes: []
            }
            this.state.nModels++;
            this.state.tree.push(newModel)
            this.setState((state) => {
                return { tree: state.tree };
            });
        })
    }

    // The explorer works like a stack at the moment, this is the pop operation
    // (TODO) Should be the SOM container that is selected by the user
    saveNewModel() {
        if (this.state.nModels > 0) {
            let somContainer = this.state.tree[this.state.nModels-1];
            window.pywebview.api.call_service(this.props.datastore, "save_som_container", [somContainer]).then((finish) => {
                if (finish) {
                    this.state.tree.pop();
                    this.setState((state) => {
                        return { tree: state.tree };
                    })
                }
            });
        }
    }

    addDataInstance() {
        if (this.state.nModels > 0) {
            window.pywebview.api.call_service(this.props.datastore, "open_csv_file_instance", []).then((descriptor) => {
                // (TODO) Should be the SOM container that is selected by the user
                if (descriptor == null) {
                    return;
                }
                let som_label = this.state.tree[this.state.nModels-1].label;
                let newInstance = {
                    icon: "database",
                    label: descriptor,
                }
                window.pywebview.api.call_service(this.props.datastore, "add_file_to_som", [som_label, descriptor]).then((finish) => {
                    if (finish) {
                        // (TODO) Should be the SOM container that is selected by the user
                        this.state.tree[this.state.nModels-1].childNodes.push(newInstance);
                        this.setState((state) => {
                            return { tree: state.tree };
                        });
                    }
                })
            });
        }
    }

    updateTree(thing){
        thing()
        this.setState({tree: this.state.tree})
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
                    contents={this.state.tree}

                />


            </>)

    }
}

export default ProjectExplorer;
