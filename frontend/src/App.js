import React from 'react';

import TopNav from './components/TopNav';
import PlayerOverview from './components/pages/PlayerOverview';

import { Route, Switch } from 'react-router-dom';

import './style/main.css';

export default function App() {
  return (
    <div className="container">
      <TopNav />
      <Switch>
        <Route path='/players'>
          <PlayerOverview />
        </Route>
      </Switch>
    </div>
  );
};