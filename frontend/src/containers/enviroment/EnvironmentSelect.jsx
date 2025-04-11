import React, {useEffect} from 'react';
import {Fab, Icon, IconButton, MenuItem, TextField} from "@mui/material";
import Box from "@mui/material/Box";
import {SettingPopup} from "./settingPopup/SettingPopup";
import {useEnvSliceSelector, useEnvSlice} from "./slice";
import {useDispatch} from "react-redux";


export const EnvironmentSelect = () => {
    const {actions} = useEnvSlice();
    const dispatch = useDispatch();
    const selected = useEnvSliceSelector((state) => state.selected);
    const ids = useEnvSliceSelector((state) => state.ids);
    const [open, setOpen] = React.useState(false)

    useEffect(() => {
      dispatch(actions.fetch({}))
    }, [])

    function handleSelect(event) {
      dispatch(actions.saveSelected({selected: event.target.value}))
    }

    return (
      <>
        {
          ids.length ?
            <Box sx={{display: 'flex', alignItems: 'center'}}>
              <TextField
                sx={{minWidth: '188px'}}
                label="Environment"
                name="environment"
                size="small"
                variant="outlined"
                color="secondary"
                select
                value={selected}
                onChange={handleSelect}
              >
                {ids.map((item) => (
                  <MenuItem value={item} key={item}>
                    {item}
                  </MenuItem>
                ))}
              </TextField>
              <Fab
                onClick={() => setOpen(true)}
                color="primary"
                component="span"
                size='medium'
                sx={{
                  boxShadow: 'none',
                  transition: 'all 250ms',
                  '&:hover': {
                    background: 'background.paper',
                    color: '#ffffff',
                    backgroundColor: 'background.paper',
                    fallbacks: [{color: 'white !important'}],
                  }
                }}
              >
                <IconButton
                  size='medium'
                  color="secondary"
                >
                  <Icon>settings</Icon>
                </IconButton>
              </Fab>
              <SettingPopup
                open={open}
                setOpen={setOpen}
                env={selected}
              />
            </Box> : <></>
        }
      </>
    )
  }
;
