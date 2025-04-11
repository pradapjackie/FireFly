import React from 'react';
import Menu from '@mui/material/Menu';
import {ThemeProvider, StyledEngineProvider, Box} from '@mui/material'
import {mainTheme} from "styles/Themes";


export const CustomMenu = (props) => {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const children = React.Children.toArray(props.children);
  const {shouldCloseOnItemClick = true, horizontalPosition = 'left'} = props;

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return <>
    <Box
      sx={{
        display: 'inline-block',
        color: 'text.primary',
        '& div:hover': {
          backgroundColor: 'action.hover',
        },
      }}
      onClick={handleClick}
    >
      {props.menuButton}
    </Box>
    <StyledEngineProvider injectFirst>
      <ThemeProvider theme={mainTheme}>
        <Menu
          elevation={8}
          anchorEl={anchorEl}
          open={!!anchorEl}
          onClose={handleClose}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: horizontalPosition,
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: horizontalPosition,
          }}
        >
          {children.map((child, index) => (
            <div
              onClick={shouldCloseOnItemClick ? handleClose : () => {
              }}
              key={index}
            >
              {child}
            </div>
          ))}
        </Menu>
      </ThemeProvider>
    </StyledEngineProvider>
  </>;
};
