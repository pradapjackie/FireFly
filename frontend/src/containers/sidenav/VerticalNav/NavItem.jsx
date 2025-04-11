import {NavLink} from 'react-router-dom';
import TouchRipple from '@mui/material/ButtonBase';
import React from 'react';
import {Box, Icon} from "@mui/material";

const NavIcon = ({icon}) => (
  <Icon sx={{fontSize: '18px', verticalAlign: 'middle', width: '36px', paddingLeft: '1rem', paddingRight: '1rem'}}>
    {icon}
  </Icon>
);

export const VerticalNavItem = ({sidebarMode, item}) => {
  const {name, path, icon, iconText} = item
  const isCompact = sidebarMode === 'compact';

  return (
    <Box
      component={NavLink}
      to={path}
      name="NavLinkItem"
      exact={true}
      sx={[
        {
          display: 'flex',
          justifyContent: 'space-between',
          height: '44px',
          borderRadius: '4px',
          marginBottom: '0.5rem',
          whiteSpace: 'pre',
          overflow: 'hidden',
          transition: 'all 150ms ease-in',
          '&:hover': {
            backgroundColor: 'action.hover',
          },
          "&.active": {backgroundColor: "action.selected"}
        },
        isCompact && {
          overflow: 'hidden',
          justifyContent: 'center !important',
        }
      ]}
      className='compactNavItem'
    >
      <TouchRipple key={name} sx={{width: '100%'}}>
        {icon ? (
          <NavIcon icon={icon} iconText={iconText}/>
        ) : isCompact ? (
          <>
            <Box
              sx={{
                backgroundColor: 'text.secondary',
                padding: '2px',
                borderRadius: '300px',
                overflow: 'hidden',
                marginLeft: '1.5rem',
                marginRight: '0.5rem',
                display: 'none'
              }}
              className='sidenavHoverShow'
            />
            <Box sx={{marginLeft: '1.25rem', fontSize: '11px'}} className='navBulletText'>
              {' '}
              {iconText}{' '}
            </Box>
          </>
        ) : (
          <Box
            sx={{
              backgroundColor: 'text.secondary',
              padding: '2px',
              borderRadius: '300px',
              overflow: 'hidden',
              marginLeft: '1.5rem',
              marginRight: '0.5rem',
            }}
          />
        )}
        <Box
          component={'span'}
          sx={[
            {
              verticalAlign: 'middle',
              textAlign: 'left',
              fontSize: '0.875rem',
              paddingLeft: '0.8rem',
            },
            isCompact && {display: 'none'}
          ]}
          className='sidenavHoverShow'
        >
          {' '}
          {name}{' '}
        </Box>
        <Box sx={{marginLeft: 'auto', marginRight: 'auto'}}/>
      </TouchRipple>
    </Box>
  );
};
