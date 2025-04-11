import React from 'react';
import { ThemeProvider, StyledEngineProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import CssVars from './cssVars';
import {mainTheme} from "styles/Themes";

const GlobalTheme = ({ children }) => {

  return (
    <StyledEngineProvider injectFirst>
      <ThemeProvider theme={mainTheme}>
        <CssBaseline />
        <CssVars> {children} </CssVars>
      </ThemeProvider>
    </StyledEngineProvider>
  );
};

export default GlobalTheme;
