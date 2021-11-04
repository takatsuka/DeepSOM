
import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuItem, Position, Button, Divider, ButtonGroup, Tab, Tabs, Intent, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay } from "@blueprintjs/core";

import "./creator.scss"
import Welcome from "../welcome/welcome"
import ScatterView3D from "../scatterview_3d/scatterview"
import DragDropSOM from '../drag-drop/drag-drop';
import ImageView from '../imageview/imageview';

import ProjectExplorer from '../project_explorer/project_explorer';

import SplitPane, { Pane } from 'react-split-pane';

import TabsManager from '../common/tabsmanager';

import "../common/splitview.scss"

class Creator extends Component {
  constructor(props) {
    super(props)

    this.launchDatastore = this.launchDatastore.bind(this)

    this.tabman = React.createRef();
    this.explorerman = React.createRef();

    this.state = {
      tab: "sum", temp_vizData: [[1.0, 1.0, 1.0], [-1.0, -1.0, -1.0]],
      tabs: [],
      datastore: null,
    }
  }

  componentDidMount() {
    window.addEventListener('pywebviewready', this.launchDatastore)
  }

  onTabChange(x) {
    this.setState({ tab: x })
    if (x === "tag") this.getTags()
  }

  onTabsUpdated(list) {
    this.setState({ tabs: list, tab: list[0].id })
  }

  launchDatastore() {
    window.pywebview.api.launch_service("SOMDatastoreService").then((ds) => {
      this.setState({ datastore: ds })
    })
    
  }

  requestTerminate() {
    window.removeEventListener('pywebviewready', this.launchDatastore)
    window.pywebview.api.terminate()
  }

  embedCard(whatever) {
    return (
      <Card interactive={false} elevation={Elevation.TWO}>
        {whatever}
      </Card>
    )
  }

  render() {

    const fileMenu = (
      <Menu>
        <MenuItem icon="label" text="Open Workspace" onClick={() => { this.explorerman.current.loadWorkspace() }} />
        <MenuItem icon="git-repo" text="New Workspace" onClick={() => { this.explorerman.current.createNewWorkspace() }} />
        <MenuItem icon="git-push" text="Save Workspace" onClick={() => { this.explorerman.current.saveWorkspace() }} />
        <Divider />
        <MenuItem icon="database" text="Import Data" onClick={() => { this.explorerman.current.importData() }} />
        <MenuItem icon="polygon-filter" text="Import Model" onClick={() => { this.explorerman.current.addSOM() }} />
      </Menu>
    )

    const viewMenu = (
      <Menu>
        <MenuItem icon="chat" text="Welcome" onClick={() => { this.tabman.current.openTab(<Welcome />, "Welcome PySOM", true) }} />
        <Divider />
        <MenuItem icon="layout-auto" text="Editor" onClick={() => { this.tabman.current.openTab(<DragDropSOM />, "Editor", true) }}/>
        <Divider />
        <MenuItem icon="heatmap" text="Scatter" onClick={() => { this.tabman.current.openTab(<ScatterView3D />, "Scatter", true, this.state.datastore) }}/>
        <MenuItem icon="media" text="Image" onClick={() => { this.tabman.current.openTab(<ImageView />, "Image", true) }}/>
      </Menu>
    )

    return (
      <>

        <Overlay isOpen={this.state.spinning_overlay} >
          <div className='loading-overlay'>
            <Card className="loading-overlay-card">
              <Spinner intent={Intent.PRIMARY} />
            </Card>
          </div>
        </Overlay>

        <Navbar className="navbar bp3-dark pywebview-drag-region">
          <Navbar.Group align={Alignment.LEFT}>
            <Navbar.Heading>PySOM Creator</Navbar.Heading>
            <Navbar.Divider />

            <Popover content={fileMenu} position={Position.BOTTOM_LEFT} interactionKind="click">
              <Button className="bp3-minimal" icon="document" text="File" />
            </Popover>

            <Popover content={viewMenu} position={Position.BOTTOM_LEFT} interactionKind="click">
              <Button className="bp3-minimal" icon="control" text="View" />
            </Popover>


            <Button className="bp3-minimal" icon="help" text="Help" />

          </Navbar.Group>

          <Navbar.Group align={Alignment.RIGHT}>
            <Button className="bp3-minimal" icon="cross" onClick={() => this.requestTerminate()} />
          </Navbar.Group>
        </Navbar>

        <div className="detail">
          <SplitPane split="vertical" minSize={180} style={{height:'calc(100% - 50px)'}} >

            <div className="leftpanel">
              <ProjectExplorer ref={this.explorerman} datastore={this.state.datastore} />

            </div>

            <div className="detail-inner">

              <div className="submenubar">
                <Tabs id="TabsExample" onChange={(x) => { this.onTabChange(x) }} selectedTabId={this.state.tab}>
                  {this.state.tabs.map((t) => (
                    <Tab id={t.id} key={t.id} title={t.dname}> <Icon icon="small-cross" onClick={() => this.tabman.current.closeTab(t.id)}/> </Tab>
                  ))}
                </Tabs>
              </div>
              <div className="submenu-spacer" />

              <div className="detail-container">
                <TabsManager ref={this.tabman}
                  activeTab={this.state.tab}
                  onTabsListChanged={(x) => this.onTabsUpdated(x)} 
                  onSwitch={(x) => this.onTabChange(x)}/>
              </div>

            </div>


          </SplitPane>
        </div>




      </>)

  }
}

export default Creator;
