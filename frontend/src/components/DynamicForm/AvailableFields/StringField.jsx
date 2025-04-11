import React, { useMemo } from 'react';
import { TextField } from '@mui/material';
import { useFormContext } from '../DynamicFormContext';

export const StringField = ({ alias, placeholder, defaultValue, valid, optional }) => {
    const [formContext, handleFormChange] = useFormContext();
    const label = optional ? 'Optional *' : placeholder;

    const onChange = (event) => {
        handleFormChange(alias, event.target.value);
    };

    const renderComponent = () => {
        return (
            <TextField
                error={valid === false}
                label={label}
                size="small"
                variant="outlined"
                value={formContext[alias] || defaultValue || ''}
                onChange={onChange}
                fullWidth
                InputLabelProps={optional ? { shrink: true } : {}}
            />
        );
    };
    return useMemo(renderComponent, [formContext[alias], valid]);
};
