import React from 'react';
import { useDispatch } from 'react-redux';
import { actions, useRunAutotestSliceSelector } from '../../../slice';
import { Checkbox, FormControlLabel } from '@mui/material';

export const ItemContentT = ({ itemId, stateSubFolderName }) => {
    const dispatch = useDispatch();
    const { name, selected } = useRunAutotestSliceSelector(stateSubFolderName, (state) => state.items.entities[itemId]);
    const handleCheckboxSelection = () => {
        dispatch(actions.testSelected({ testId: itemId, value: !selected, stateSubFolderName: stateSubFolderName }));
    };

    return (
        <FormControlLabel
            onClick={(event) => event.stopPropagation()}
            onFocus={(event) => event.stopPropagation()}
            control={<Checkbox checked={selected} onChange={handleCheckboxSelection} />}
            label={name}
        />
    );
};
export const ItemContent = React.memo(ItemContentT);
