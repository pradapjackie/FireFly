import React, { useMemo } from 'react';
import { Checkbox, FormControlLabel } from '@mui/material';
import { useFormContext } from '../DynamicFormContext';
import _ from 'lodash';

export const CheckboxField = ({ alias, placeholder, defaultValue }) => {
    const [formContext, handleFormChange] = useFormContext();

    const onChange = (event) => {
        event.persist();
        handleFormChange(alias, event.target.checked);
    };

    const renderComponent = () => {
        return (
            <FormControlLabel
                control={
                    <Checkbox
                        checked={_.isUndefined(formContext[alias]) ? defaultValue : formContext[alias]}
                        onChange={onChange}
                    />
                }
                label={placeholder}
            />
        );
    };

    return useMemo(renderComponent, [formContext[alias]]);
};
