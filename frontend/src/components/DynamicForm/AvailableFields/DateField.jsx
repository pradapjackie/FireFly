import { enGB } from 'date-fns/locale';
import React, { useMemo } from 'react';
import { useFormContext } from '../DynamicFormContext';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import {format, parseISO} from 'date-fns';

export const DateField = ({ alias, placeholder, defaultValue, valid, optional }) => {
    const [formContext, handleFormChange] = useFormContext();
    const label = optional ? 'Optional *' : placeholder;
    const currentValue = formContext[alias] ? parseISO(formContext[alias]) : null
    defaultValue = defaultValue ? parseISO(defaultValue) : null;

    const onChange = (newValue) => {
        handleFormChange(alias, format(newValue, 'yyyy-MM-dd'));
    };

    const renderComponent = () => {
        return (
            <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={enGB}>
                <DatePicker
                    slotProps={{ textField: { size: 'small', error: valid === false, fullWidth: true } }}
                    label={label}
                    value={currentValue || defaultValue || null}
                    onChange={onChange}
                />
            </LocalizationProvider>
        );
    };
    return useMemo(renderComponent, [formContext[alias], valid]);
};
