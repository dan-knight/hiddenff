import React, { createRef, forwardRef, useEffect, useState } from 'react';
import Divider from './Divider';

export default function Accordion({ label, collapseID, ...props }) {
  const [isClosed, height, ref, handleToggle] = useCollapse();

  return (
    <div className={'accordion' + (props.cssClass ? ` ${props.cssClass}` : '')}>
      <div className='top'>
        <Toggle label={label} onToggle={handleToggle} />
        {props.topExtras}
      </div>
      <Content isClosed={isClosed} height={height} ref={ref}>
        {props.children}
      </Content>
      <Divider />
    </div>
  );
};

function Toggle({ label, onToggle }) {
  return (
    <div className="toggle" onClick={onToggle}>
      <h5>{label}</h5>
    </div>
  );
};

const Content = forwardRef((props, ref) => (
    <div ref={ref} className={"content" + (props.isClosed ? ' closed' : '')} style={props.height ? { height: props.height } : null}>
      <div className="wrapper">
      {props.children}
      </div>
    </div>
  )); 

function useCollapse() {
  const [isClosed, setClosed] = useState(false);
  const [height, setHeight] = useState(null);

  const ref = createRef();
  let transitionTimeout;

  function handleToggle() {
    clearTimeout(transitionTimeout);

    const currentHeight = ref.current.clientHeight;
    setHeight(currentHeight);

    const toClose = !isClosed;
    setClosed(toClose);
    
    if (!toClose) {
      const targetHeight = ref.current.firstChild.clientHeight;
      setHeight(targetHeight);

      const durationSeconds = window.getComputedStyle(ref.current).getPropertyValue('transition-duration').match(/\d/g);
      transitionTimeout = setTimeout(() => setHeight(null), durationSeconds * 1000);
    }    
  }

  useEffect(() => {
    if (isClosed) {
      setHeight(null);
    }
  });

  return [isClosed, height, ref, handleToggle];
}