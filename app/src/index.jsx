import React from 'react'
import ReactDOM from 'react-dom'

import Creator from './components/creator/Creator'

import './index.scss'

import "@blueprintjs/core/lib/css/blueprint.css";
import 'normalize.css';

const App = function() {
  return (
    <>
      <Creator />
    </>
  )
}

const view = App('PySOM Creator')

const element = document.getElementById('app')
ReactDOM.render(view, element)