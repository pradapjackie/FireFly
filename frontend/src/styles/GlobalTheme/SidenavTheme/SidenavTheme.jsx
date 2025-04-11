import React from 'react';
import { ThemeProvider, StyledEngineProvider } from '@mui/material/styles';
import {secondaryTheme} from "styles/Themes";

const SidenavTheme = ({ children }) => {

  return (
    <StyledEngineProvider injectFirst>
      <ThemeProvider theme={secondaryTheme}>{children}</ThemeProvider>
    </StyledEngineProvider>
  );
};

export default SidenavTheme;
