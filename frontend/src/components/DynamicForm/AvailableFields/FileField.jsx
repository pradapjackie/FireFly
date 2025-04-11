import React, { useMemo, useState } from 'react';
import { useFormContext } from '../DynamicFormContext';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { Box, Button, TextField } from '@mui/material';

export const FileField = ({ alias, valid }) => {
    const [formContext, handleFormChange] = useFormContext();
    const [fileName, setFileName] = useState('');
    const onChange = (event) => {
        const file = event.target.files[0];
        setFileName(event.target.value);
        if (file) {
            const reader = new FileReader();
            reader.onload = (readEvent) => {
                handleFormChange(alias, {fileName: event.target.value, data: readEvent.target.result});
            };
            reader.readAsDataURL(file);
        }
    };

    const renderComponent = () => {
        return (
            <Box sx={{ display: 'flex', width: '100%' }}>
                <TextField
                    disabled
                    fullWidth
                    size="small"
                    variant="outlined"
                    value={fileName}
                    sx={[
                        valid === false && {
                            '& .MuiInputBase-root.Mui-disabled': {
                                '& > fieldset': {
                                    borderColor: 'error.main',
                                },
                            },
                        },
                    ]}
                />
                <Button
                    component="label"
                    role={undefined}
                    variant="outlined"
                    tabIndex={-1}
                    startIcon={<CloudUploadIcon />}
                    sx={{ '& .MuiButton-startIcon': { margin: '0' } }}
                >
                    <input type="file" hidden onChange={onChange} />
                </Button>
            </Box>
        );
    };
    return useMemo(renderComponent, [formContext[alias], valid]);
};
