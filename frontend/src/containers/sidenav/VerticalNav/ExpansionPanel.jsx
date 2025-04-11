import React, {useState, useRef, useCallback, useEffect} from 'react';
import {Box, Icon} from '@mui/material';
import TouchRipple from '@mui/material/ButtonBase';
import {useLocation} from 'react-router-dom';

export const ExpansionPanel = ({item, children, mode}) => {
  const [collapsed, setCollapsed] = useState(true);
  const elementRef = useRef(null);
  const componentHeight = useRef(0);
  const {pathname} = useLocation();
  const {name, icon, iconText} = item;

  const handleClick = () => {
    componentHeight.current = 0;
    calculateHeight(elementRef.current);
    setCollapsed(!collapsed);
  };

  const calculateHeight = useCallback((node) => {
    if (node.name === 'NavLinkItem') {
      componentHeight.current += node.scrollHeight + parseInt(window.getComputedStyle(node).marginBottom) + parseInt(window.getComputedStyle(node).marginTop);
    } else {
      for (const child of node.children) {
        calculateHeight(child);
      }
    }
  }, []);

  useEffect(() => {
    if (!elementRef) return;
    calculateHeight(elementRef.current);
    // Open dropdown if child is active
    for (const child of elementRef.current.children) {
      if (child.getAttribute('href') === pathname) {
        setCollapsed(false);
      }
    }
  }, [pathname, calculateHeight]);

  return (<div>
    <TouchRipple
      sx={[{
        display: 'flex',
        justifyContent: 'space-between',
        height: '44px',
        borderRadius: '4px',
        marginBottom: '0.5rem',
        width: '100%',
        paddingRight: '1rem',
        whiteSpace: 'pre',
        overflow: 'hidden',
        '&:hover': {
          backgroundColor: 'action.hover',
        },
      }, mode === 'compact' && {
        width: 44, overflow: 'hidden',
      }]}
      className='compactNavItem'
      onClick={handleClick}
    >
      <Box sx={{display: 'flex', alignItems: 'center'}}>
        {icon && (<Icon sx={{
          verticalAlign: 'middle', fontSize: '18px', width: '36px', paddingLeft: '1rem', paddingRight: '1rem'
        }}> {icon} </Icon>)}
        {iconText && (<Box
          sx={{
            borderRadius: '300px',
            overflow: 'hidden',
            width: '4px',
            height: '4px',
            background: 'text.secondary',
            marginLeft: '1rem',
            marginRight: '0.5rem'
          }}
        />)}
        <Box
          componens="span"
          sx={{
            verticalAlign: 'middle', fontSize: '0.875rem', paddingLeft: '0.8rem',
          }}
          className='sidenavHoverShow'
        >
          {name}
        </Box>
      </Box>
      <Box
        sx={[
          collapsed && {
            transition: 'transform 0.3s cubic-bezier(0, 0, 0.2, 1) 0ms',
            transform: 'rotate(0deg)',
          },
          !collapsed && {
            transition: 'transform 0.3s cubic-bezier(0, 0, 0.2, 1) 0ms',
            transform: 'rotate(90deg)',
          }
        ]}
        className='sidenavHoverShow'
      >
        <Icon fontSize="small" sx={{verticalAlign: 'middle'}}>
          {' '}
          chevron_right{' '}
        </Icon>
      </Box>
    </TouchRipple>

    <Box
      ref={elementRef}
      sx={[
        {
          overflow: 'hidden',
          transition: 'max-height 0.3s cubic-bezier(0, 0, 0.2, 1)',
        },
        collapsed ? {maxHeight: '0px'} : {maxHeight: `${componentHeight.current}px`}

      ]}
    >
      {children}
    </Box>
  </div>);
};
