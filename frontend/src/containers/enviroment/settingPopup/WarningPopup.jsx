import React from 'react';
import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    List,
    ListItem,
    ListItemText,
    ListItemIcon,
    Divider,
} from '@mui/material';
import LabelIcon from '@mui/icons-material/Label';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { SimpleTable } from '../../../components/SimpleTable';

const arrow = ' \u{2192} ';

const UpdatedParam = ({ item }) => {
    let data = {};
    if (item.value !== item.initial.value) {
        data['Value'] = `${item.initial.value} ${arrow} ${item.value}`;
    }
    if (item.secure !== item.initial.secure) {
        data['Secure'] = `${item.initial.secure} ${arrow} ${item.secure}`;
    }

    return (
        <ListItem primary={item.param}>
            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                <Box
                    sx={{
                        display: 'flex',
                        flexDirection: 'row',
                        alignItems: 'center',
                    }}
                >
                    <ListItemIcon sx={{ minWidth: '40px' }}>
                        <LabelIcon />
                    </ListItemIcon>
                    <ListItemText primary={item.param} />
                </Box>
                <Box sx={{ paddingLeft: '40px' }}>
                    <SimpleTable data={data} stringify={false} />
                </Box>
            </Box>
        </ListItem>
    );
};

const RemovedParam = ({ item }) => {
    return (
        <ListItem primary={item}>
            <ListItemIcon sx={{ minWidth: '40px' }}>
                <LabelIcon />
            </ListItemIcon>
            <ListItemText primary={item} />
        </ListItem>
    );
};

export const EnvWarningPopupT = ({ open, setOpen, save, data }) => {
    return (
        <Dialog open={open} maxWidth={'md'} onClose={() => setOpen(false)}>
            <DialogTitle>{'Please confirm environment settings changes for everyone.'}</DialogTitle>
            <DialogContent>
                <Typography sx={{ marginBottom: '1rem' }}>
                    You are going to change "Default" values of the following parameters for all FireFly users.
                </Typography>
                <Typography sx={{ marginBottom: '1rem' }}>
                    If the environment settings have actually changed - click "Confirm"
                </Typography>
                <Typography>
                    If you only want to change values for yourself - click "Cancel" and change values in "Current"
                    column.
                </Typography>
                <Typography>
                    Settings will be saved in your browser Local storage and you can continue to use them until your
                    browser data is cleared.
                </Typography>
                <Divider sx={{ marginTop: '1rem', marginBottom: '1rem' }} />
                {data.updated.length > 0 && (
                    <>
                        <Typography variant="subtitle1">Will be updated:</Typography>
                        <List dense={true}>
                            {data.updated.map((item) => (
                                <UpdatedParam key={item.param} item={item} />
                            ))}
                        </List>
                    </>
                )}
                {data.deleted.length > 0 && (
                    <>
                        <Typography variant="subtitle1">Will be removed:</Typography>
                        <List dense={true}>
                            {data.deleted.map((item) => (
                                <RemovedParam key={item} item={item} />
                            ))}
                        </List>
                    </>
                )}
            </DialogContent>
            <DialogActions>
                <Button color="secondary" variant="contained" onClick={save}>
                    Confirm
                </Button>
                <Button color="secondary" variant="contained" onClick={() => setOpen(false)}>
                    Cancel
                </Button>
            </DialogActions>
        </Dialog>
    );
};
export const EnvWarningPopup = React.memo(EnvWarningPopupT);
