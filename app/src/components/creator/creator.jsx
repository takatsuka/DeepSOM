
import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuDivider, MenuItem, Position, Button, Divider, ButtonGroup, Tab, Tabs, Intent, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay, Switch } from "@blueprintjs/core";

// https://stackoverflow.com/a/52814399
import { FocusStyleManager } from "@blueprintjs/core";
FocusStyleManager.onlyShowFocusOnTabs();

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
      dark: true,
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

  darkModeToggle() {
    if (this.state.dark) {
      document.body.classList.remove('bp3-dark');
    } else {
      document.body.classList.add('bp3-dark');
    }
    this.setState(prevState => ({dark: !prevState.dark}));
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
        <MenuDivider title="Create" />
        <MenuItem icon="layout-auto" text="New Model" onClick={() => { this.explorerman.current.newSOM(true) }} />
        <MenuDivider title="Workspace" />
        <MenuItem icon="label" text="Open" onClick={() => { this.explorerman.current.loadWorkspace() }} />
        <MenuItem icon="git-repo" text="New" onClick={() => { this.explorerman.current.createNewWorkspace() }} />
        <MenuItem icon="git-push" text="Save" onClick={() => { this.explorerman.current.saveWorkspace() }} />
        <MenuDivider title="Dataset" />
        <MenuItem icon="database" text="Import Data" onClick={() => { this.explorerman.current.importData() }} />
        <MenuItem icon="polygon-filter" text="Import Model" onClick={() => { this.explorerman.current.addSOM() }} />

        <MenuDivider title="DEBUG" />
        <MenuItem icon="database" text="Picker" onClick={() => { this.explorerman.current.ask_user_pick_data("Select a data to do nothing.","matrix", (k) => console.log(k)) }} />
      </Menu>
    )

    const viewMenu = (
      <Menu>

        <MenuItem icon="chat" text="Welcome" onClick={() => { this.tabman.current.openTab(<Welcome />, "Welcome PySOM", true) }} />
        <Divider />
        <MenuItem icon="layout-auto" text="Editor" onClick={() => { this.tabman.current.openTab(<DragDropSOM />, "untitled", true) }} />
        <MenuDivider title="Visualization" />
        <MenuItem icon="heatmap" text="Scatter" onClick={() => { this.tabman.current.openTab(<ScatterView3D />, "Scatter", true, this.state.datastore) }} />
        <MenuItem icon="media" text="Image" onClick={() => { this.tabman.current.openTab(<ImageView />, "Image", true) }} />
        <MenuDivider title="Appearance" />
        <Switch style={{marginLeft:"10px", marginTop:"10px"}} large checked={this.state.dark} innerLabel="Light" innerLabelChecked="Dark" onChange={() => this.darkModeToggle()} />
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
              <Button className="bp3-minimal" icon="document" text="File" id="file-btn" />
            </Popover>

            <Popover content={viewMenu} position={Position.BOTTOM_LEFT} interactionKind="click">
              <Button className="bp3-minimal" icon="control" text="View" id="view-btn" />
            </Popover>


            <Button className="bp3-minimal" icon="help" text="Help" id="help-btn" />

          </Navbar.Group>

          <Navbar.Group align={Alignment.RIGHT}>
            <Button className="bp3-minimal" icon="cross" onClick={() => this.requestTerminate()} />
          </Navbar.Group>
        </Navbar>

        <div className="detail">
          <SplitPane split="vertical" minSize={180} style={{ height: 'calc(100% - 50px)' }} >

            <div className="leftpanel">
              <ProjectExplorer ref={this.explorerman} datastore={this.state.datastore}
                openTab={(a, b, c, d) => this.tabman.current.openTab(a, b, c, d)}
              />

            </div>

            <div className="detail-inner">

              <div className="submenubar">
                <Tabs id="TabsExample" onChange={(x) => { this.onTabChange(x) }} selectedTabId={this.state.tab}>
                  {this.state.tabs.map((t) => (
                    <Tab id={t.id} key={t.id} title={t.dname}> <Icon icon="small-cross" onClick={() => this.tabman.current.closeTab(t.id)} /> </Tab>
                  ))}
                </Tabs>
              </div>
              <div className="submenu-spacer" />

              <div className="detail-container">
                <TabsManager ref={this.tabman}
                  activeTab={this.state.tab}
                  onTabsListChanged={(x) => this.onTabsUpdated(x)}
                  onSwitch={(x) => this.onTabChange(x)}
                  fileman={this.explorerman.current} />
              </div>

            </div>


          </SplitPane>
        </div>




      </>)

  }
}

export default Creator;
