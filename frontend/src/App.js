import React, { useEffect, useState } from 'react';

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
      <nav>
        <h1>Hello world</h1>
      </nav>
    </React.Fragment>
  );
};