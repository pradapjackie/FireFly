import React, { useMemo } from 'react';
import { TextField } from '@mui/material';
import { useFormContext } from '../DynamicFormContext';

export const NumberField = ({ alias, placeholder, defaultValue, valid, optional }) => {
    const [formContext, handleFormChange] = useFormContext();
    const label = optional ? 'Optional *' : placeholder;

    const onChange = (event) => {
        event.persist();
        handleFormChange(alias, event.target.value);
    };

    const renderComponent = () => {
        return (
            <TextField
                error={valid === false}
                label={label}
                type="number"
                size="small"
                variant="outlined"
                fullWidth
                value={formContext[alias] || defaultValue || ''}
                onChange={onChange}
                InputLabelProps={{ shrink: true }}
            />
        );
    };

    return useMemo(renderComponent, [formContext[alias], valid]);
};
