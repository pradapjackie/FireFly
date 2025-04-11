import React, { useMemo } from 'react';
import { TextField } from '@mui/material';
import { Autocomplete } from '@mui/material';
import { useFormContext } from '../DynamicFormContext';

export const AutocompleteField = ({ alias, placeholder, options, defaultValue, valid, optional }) => {
    const [formContext, handleFormChange] = useFormContext();
    const label = optional ? 'Optional *' : placeholder;

    const onChange = (event, value) => {
        event.persist();
        handleFormChange(alias, value);
    };

    const renderComponent = () => {
        return (
            <Autocomplete
                options={options}
                value={formContext[alias] || defaultValue}
                onChange={onChange}
                renderInput={(params) => (
                    <TextField
                        {...params}
                        error={valid === false}
                        label={label}
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
