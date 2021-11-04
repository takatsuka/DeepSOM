
import * as React from 'react'
import { Component } from 'react';

import { Classes, Icon, Intent, TreeNodeInfo, Tree, Elevation, Card, Button, ButtonGroup } from "@blueprintjs/core";
import { Classes as Popover2Classes, ContextMenu2, Tooltip2 } from "@blueprintjs/popover2";
import { TAG_INPUT_VALUES } from '@blueprintjs/core/lib/esm/common/classes';


class ProjectExplorer extends Component {
    constructor(props) {
        super(props)

        this.state = {
            workspaceName: "new",
            tree: [
                {
                    isExpanded: false,
                    icon: "folder-close",
                    label: 'Objects',
                    childNodes: []
                },
                {
                    isExpanded: false,
                    icon: "folder-close",
                    label: 'Models',
                    childNodes: []
                },
            ],
        }
    }

    componentDidMount() {

    }

    refresh() {
        window.pywebview.api.call_service(this.props.datastore, "current_workspace_name", []).then((e) => {
            this.setState({
                workspaceName: e
            });
        });

        window.pywebview.api.call_service(this.props.datastore, "fetch_objects", ["matrix"]).then((e) => {
            let l = e.map((e, id) => ({
                id: id,
                hasCaret: false,
                icon: "database",
                label: e,  
            }))

            this.state.tree[0].childNodes = l
            this.setState({tree: this.state.tree})
        });
    }

    loadWorkspace() {
        window.pywebview.api.call_service(this.props.datastore, "load_workspace", []).then(() => {
            this.refresh()
        })
    }

    createNewWorkspace() {
        window.pywebview.api.call_service(this.props.datastore, "new_workspace", []).then((e) => {
            this.refresh()
        });
    }

    saveWorkspace() {
        window.pywebview.api.call_service(this.props.datastore, "save_current_workspace", []).then((name) => {
            this.refresh()
        });
    }

    importData() {
        window.pywebview.api.call_service(this.props.datastore, "import_data_from_csv", []).then(() => {
            this.refresh()
        });
    }

    addSOM() {
        window.pywebview.api.call_service(this.props.datastore, "import_model", []).then((descriptor) => {
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

    updateTree(thing) {
        thing()
        this.setState({ tree: this.state.tree })
    }

    render() {

        return (
            <>
                <ButtonGroup minimal={false} elevation={Elevation.FOUR} fill={true} alignText="left" minimal={true} large={true}>
                    <Button active={true} >{this.state.workspaceName}</Button>

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
