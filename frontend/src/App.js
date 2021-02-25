import React from 'react';

import TopNav from './components/TopNav';
import PlayerOverview from './components/PlayerOverview';

import './style/main.css';

export default function App() {
  return (
    <div className="container">
      <TopNav />
      <PlayerOverview />
    </div>
  );
};