import {createTheme} from "@mui/material/styles";
import {deepmerge} from "@mui/utils";
import themeOptions from "./themeOptions";

const textLight = {
  primary: 'rgba(52, 49, 76, 1)',
  secondary: 'rgba(52, 49, 76, 0.54)',
  disabled: 'rgba(52, 49, 76, 0.38)',
  hint: 'rgba(52, 49, 76, 0.38)',
};
const errorColor = {
  main: '#FF3D57',
};
const successColor = {
  main: '#08AD6C',
};

export const mainTheme = createTheme(deepmerge({
    palette: {
      mode: 'dark',
      primary: {
        main: '#6a75c9',
        contrastText: '#ffffff',
      },
      secondary: {
        main: '#ff9e43',
        contrastText: textLight.primary,
      },
      error: errorColor,
      success: successColor,
      background: {
        paper: '#222A45',
        default: '#1a2038',
      },
    },
  }, themeOptions)
)

export const secondaryTheme = createTheme(deepmerge({
    palette: {
      mode: 'dark',
      primary: {
        main: '#222A45',
        contrastText: '#ffffff',
      },
      secondary: {
        main: '#7467ef',
        contrastText: '#ffffff',
      },
      error: errorColor,
      success: successColor,
      background: {
        paper: '#222A45',
        default: '#1a2038',
      },
    },
  }, themeOptions)
)
