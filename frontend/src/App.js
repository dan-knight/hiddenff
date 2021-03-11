import React from 'react';

import { TempTopNav } from './components/TopNav';
import PlayerOverview from './components/pages/PlayerOverview';

import { Route, Switch } from 'react-router-dom';

import './style/main.css';

export default function App() {
  return (
    <div className="view">
      <TempTopNav />
      <Switch>
        <Route path='/'>
          <PlayerOverview />
        </Route>
      </Switch>
    </div>
  );
};