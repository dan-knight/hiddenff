import React from 'react';
import { Link } from 'react-router-dom';

export default function TopNav() {
  return (
    <nav>
      <div>
        <Links />
        <Logo />
        <Links style={{ visibility: 'hidden' }} />
      </div>
    </nav>
  );
};

const links = [
  { url: '/players', label: 'Players' },
  { url: '/teams', label: 'Teams' },
  { url: '/settings', label: 'Settings' }
];

function Links(props) {
  return (
    <ul style={props.style}>
      {links.map(l => (
        <li key={l.url}>
          <Link to={l.url}>{l.label}</Link>
        </li>
      ))}
    </ul>
  );
};

function Logo() {
  return (
    <Link to='/'>
      <h4 align="center"><span>hidden</span>FF</h4>
    </Link>
  );
};