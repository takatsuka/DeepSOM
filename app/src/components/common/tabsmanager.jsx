import * as React from 'react'
import { Component } from 'react';
import { NonIdealState } from "@blueprintjs/core";

import Welcome from "../welcome/welcome"
import ImageView from "../imageview/imageview"
import DragDropSOM from "../drag-drop/drag-drop"
import Animal from "../animal/animal"

class TabsManager extends Component {
    constructor(props) {
        super(props)
        this.state = {
            activeTab: -1,
            openedTabs: {},

        }
        this.tabIDCounter = 0
    }

    componentDidMount() {

        this.openTab(<Welcome />, "Welcome to PySOM", true)
    }

    UNSAFE_componentWillReceiveProps(nextProps) {
        // You don't have to do this check first, but it can help prevent an unneeded render
        if (nextProps.activeTab !== this.state.activeTab) {
            this.setState({ activeTab: nextProps.activeTab });
        }
    }

    getTabInit(tabID) {
        var tabs = this.state.openedTabs
        if(tabs[tabID] == null) return // dont care about closed tabs
        if(!tabs[tabID].shouldInit) return null

        tabs[tabID].shouldInit = false
        this.setState({
            openedTabs: tabs
        })

        return tabs[tabID].init
    }

    openTab(cont, displayName, active, init) {
        var tabs = this.state.openedTabs
        let asid = this.tabIDCounter
        this.tabIDCounter = this.tabIDCounter + 1
        var c = React.cloneElement(cont, {
            key: asid,
            tabID: asid,
            fileman: this.props.fileman,
            saveState: (state) => this.storeState(asid, state),
            pullState: () => this.getState(asid),
            pullInit: () => this.getTabInit(asid)
        })

        tabs[asid] = {
            content: c,
            state: {},
            name: displayName,
            id: asid,
            init: init,
            shouldInit: init != null
        }

        this.setState({
            openTabs: tabs,
        }, () => {
            this.props.onTabsListChanged(this.getOpenedTabsDesc())
            if(active) {
                this.props.onSwitch(asid)
            }
        })
    }

    closeTab(tabID) {
        var tabIDs = Object.keys(this.state.openedTabs);
        var newActive = Math.max(tabIDs.indexOf(this.state.activeTab) - 1 , 0)
        var tabs = this.state.openedTabs
        delete tabs[tabID]
        console.log(newActive)
        newActive = tabs[Object.keys(tabs)[newActive]].id
        console.log(newActive)
        this.setState({
            openedTabs: tabs,
            activeTab: newActive
        }, () => {
            this.props.onTabsListChanged(this.getOpenedTabsDesc())
            this.props.onSwitch(newActive)
        })
    }

    storeState(tabID, state) {
        var tabs = this.state.openedTabs
        if(tabs[tabID] == null) return // dont care about closed tabs

        tabs[tabID].state = state

        this.setState({
            openedTabs: tabs
        })
    }

    getState(tabID) {
        return this.state.openedTabs[tabID].state
    }

    getOpenedTabsDesc(){
        var tabs = this.state.openedTabs
        return Object.keys(tabs).map((k) => ({id: tabs[k].id, dname: tabs[k].name}))
    }

    render() {
        if (this.state.activeTab < 0)
            return (<NonIdealState
                icon={"issue"}
                title="No tab open :("
            />)
        if (this.state.openedTabs[this.state.activeTab] == null)
            return (<NonIdealState
                icon={"ban-circle"}
                title="requested tab does not exist :("
            />)

        return (this.state.openedTabs[this.state.activeTab].content)
    }
}

export default TabsManager;
