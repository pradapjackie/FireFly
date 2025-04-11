import React, { useMemo } from 'react';
import { Chip, TextField } from '@mui/material';
import { Autocomplete } from '@mui/material';
import { useFormContext } from '../DynamicFormContext';

export const ListOfStrings = ({ alias, placeholder, defaultValue, valid, optional }) => {
    const [formContext, handleFormChange] = useFormContext();
    const label = optional ? 'Optional *' : placeholder;

    const onChange = (event, value) => {
        event.persist();
        handleFormChange(alias, value);
    };

    const renderComponent = () => {
        return (
            <Autocomplete
                multiple={true}
                freeSolo={true}
                options={[]}
                value={formContext[alias] || defaultValue || []}
                onChange={onChange}
                renderTags={(value, getTagProps) =>
                    value.map((option, index) => (
                        <Chip variant="outlined" size="small" label={option} {...getTagProps({ index })} />
                    ))
                }
                renderInput={(params) => (
                    <TextField
                        {...params}
                        error={valid === false}
                        label={label}
                        sx={{
                            '& .MuiInputBase-adornedStart': {
                                paddingTop: '3.5px !important',
                                paddingBottom: '3.5px !important',
                            },
                        }}
                        variant="outlined"
                        size="small"
                        fullWidth
                        InputLabelProps={optional ? { shrink: true } : {}}
                    />
                )}
            />
        );
    };

    return useMemo(renderComponent, [formContext[alias], valid]);
};
