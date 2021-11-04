
import * as React from 'react'
import { Component } from 'react';

import { Classes, Icon, Intent, TreeNodeInfo, Tree, Elevation, Card, Button, ButtonGroup } from "@blueprintjs/core";
import { Classes as Popover2Classes, ContextMenu2, Tooltip2 } from "@blueprintjs/popover2";
import { TAG_INPUT_VALUES } from '@blueprintjs/core/lib/esm/common/classes';


class ProjectExplorer extends Component {
    constructor(props) {
        super(props)

        this.state = {
            tree: [{
                isExpanded: true,
                icon: "folder-close",
                label: 'New Workspace',
                childNodes: []
            }],
        }
    }

    componentDidMount() {

    }

    loadWorkspace() {
        window.pywebview.api.call_service(this.props.datastore, "load_workspace", []).then((workspace) => {
            if (workspace != null) {
                let children = []
                for (let i = 0; i < workspace.data.length; i++) {
                    children.push({
                        icon: "database",
                        label: workspace.data[i],
                    })
                }

                for (let i = 0; i < workspace.som.length; i++) {
                    children.push({
                        icon: "polygon-filter",
                        label: workspace.som[i],
                    })
                }

                this.state.tree = [{
                    isExpanded: true,
                    icon: "folder-close",
                    label: workspace.label,
                    childNodes: children
                }];

                this.setState((state) => {
                    return { tree: state.tree }
                })
            }
        })
    }

    createNewWorkspace() {
        window.pywebview.api.call_service(this.props.datastore, "close_all_instances", []).then(() => {
            this.state.tree = [{
                isExpanded: true,
                icon: "folder-close",
                label: 'New Workspace',
                childNodes: []
            }];
            this.setState((state) => {
                return { tree: state.tree };
            });
        });
    }

    saveWorkspace() {
        let workspace = this.state.tree[0];
        window.pywebview.api.call_service(this.props.datastore, "save_workspace", [workspace]).then((name) => {
            if (name == null) {
                return;
            }
            this.state.tree = [{
                isExpanded: true,
                icon: 'folder-close',
                label: name,
                childNodes: workspace.childNodes
            }];
            this.setState((state) => {
                return { tree: state.tree };
            })
        });
    }

    addCsvFileToWorkspace() {
        window.pywebview.api.call_service(this.props.datastore, "open_csv_file_instance", []).then((descriptor) => {
            console.log(descriptor);
            if (descriptor == null) {
                return;
            }
            let workspaceIdentifier = this.state.tree[0].label;
            let newInstance = {
                icon: "database",
                label: descriptor,
            }
            this.state.tree[0].childNodes.push(newInstance);
            this.setState((state) => {
                return { tree: state.tree };
            });
        });
    }

    addJsonFileToWorkspace() {
        window.pywebview.api.call_service(this.props.datastore, "open_json_file_instance", []).then((descriptor) => {
            if (descriptor == null) {
                return;
            }
            let newInstance = {
                icon: "polygon-filter",
                label: descriptor,
            }
            this.state.tree[0].childNodes.push(newInstance);
            this.setState((state) => {
                return { tree: state.tree };
            });
        });
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
