import React, { useMemo } from 'react';
import { FormControlLabel, Switch } from '@mui/material';
import { useFormContext } from '../DynamicFormContext';

export const SwitchField = ({ alias, placeholder, defaultValue }) => {
    const [formContext, handleFormChange] = useFormContext();

    const onChange = (event) => {
        event.persist();
        handleFormChange(alias, event.target.checked);
    };

    const renderComponent = () => {
        return (
            <FormControlLabel
                control={<Switch checked={formContext[alias] || defaultValue} onChange={onChange} />}
                label={placeholder}
            />
        );
    };

    return useMemo(renderComponent, [formContext[alias]]);
};
