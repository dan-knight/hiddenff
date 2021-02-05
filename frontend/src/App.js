import React, { useEffect, useState } from 'react';
import TopNav from './components/TopNav';

import { getPlayers } from './requests';

import './style/main.css';

export default function App() {
  const [positions, setPositions] = useState(['RB']);
  const [sortBy, setSortBy] = useState('last');
  const [showMenu, setShowMenu] = useState(false);

  function toggleMenu() {
    setShowMenu(!showMenu);
  };

  function changePositions(value) {
    setPositions(value);
  };

  function changeSortBy(value) {
    setSortBy(value);
  };

  return (
    <React.Fragment>
      <div className="container">
        <TopNav />
        <main>main</main>
        <div className="sidebar-buffer"></div>
        <div className="sidebar">sidebar</div>
      </div>
    </React.Fragment>
  );
};