import React from 'react';
import { StringField } from './AvailableFields/StringField';
import { Box } from '@mui/material';
import { NumberField } from './AvailableFields/NumberField';
import { AutocompleteField } from './AvailableFields/AutocompleteField';
import {AutocompleteMultiField} from "./AvailableFields/AutocompleteMultiField";
import {ListOfStrings} from "./AvailableFields/ListOfStrings";
import { CheckboxField } from './AvailableFields/CheckboxField';
import { SwitchField } from './AvailableFields/SwitchField';
import { FileField } from './AvailableFields/FileField';
import { DefaultField } from './AvailableFields/DefaultField';
import { isEmpty } from 'lodash';
import { FormContextProvider } from './DynamicFormContext';
import {DateField} from "./AvailableFields/DateField";

const availableComponents = {
    string: StringField,
    number: NumberField,
    checkbox: CheckboxField,
    autocomplete: AutocompleteField,
    multi_autocomplete: AutocompleteMultiField,
    string_list: ListOfStrings,
    switch: SwitchField,
    file: FileField,
    date: DateField,
    default: DefaultField,
};

const availableComponentGroups = {};

const tableGape = '1rem';

const Section = ({ alias, type, label, fetchDynamicData, numberOfColumns, ...props }) => {
    const GroupComponent = availableComponentGroups[type];
    const FieldComponent = availableComponents[type] || availableComponents.default;

    if (GroupComponent) {
        return (
            <GroupComponent alias={alias} type={type} label={label} fetchDynamicData={fetchDynamicData} {...props} />
        );
    } else {
        return (
            <Box
                sx={{
                    flex: `calc((100% / ${numberOfColumns}) - ${tableGape} * ${
                        (numberOfColumns - 1) / numberOfColumns
                    })`,
                    display: 'flex',
                    flexGrow: '0',
                    paddingTop: '1rem',
                    alignItems: 'center',
                }}
            >
                <Box sx={{ flex: '50%', paddingRight: '1rem' }}>{label}</Box>
                <Box sx={{ flex: '50%' }}>
                    <FieldComponent alias={alias} type={type} {...props} />
                </Box>
            </Box>
        );
    }
};

export const DynamicForm = ({ requiredConfig, resultConfig, setResultConfig, fetchDynamicData, numberOfColumns = 1 }) => {
    return (
        <FormContextProvider resultConfig={resultConfig} setResultConfig={setResultConfig}>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', columnGap: tableGape }}>
                {!isEmpty(requiredConfig) ? (
                    Object.entries(requiredConfig).map(([alias, item]) => (
                        <Section
                            key={alias}
                            alias={alias}
                            fetchDynamicData={fetchDynamicData}
                            numberOfColumns={numberOfColumns}
                            {...item}
                        />
                    ))
                ) : (
                    <></>
                )}
            </Box>
        </FormContextProvider>
    );
};
