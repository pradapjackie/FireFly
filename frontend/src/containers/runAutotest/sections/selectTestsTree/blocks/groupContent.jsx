import React from 'react';
import { useDispatch } from 'react-redux';
import { actions, useRunAutotestSliceSelector } from '../../../slice';
import { Checkbox, FormControlLabel } from '@mui/material';

export const GroupContentMemo = ({ groupId, stateSubFolderName }) => {
    const dispatch = useDispatch();
    const { name, indeterminate, selected } = useRunAutotestSliceSelector(
        stateSubFolderName,
        (state) => state.groups.entities[groupId],
    );

    const handleCheckboxSelection = () => {
        const value = indeterminate ? true : !selected;
        dispatch(actions.groupSelected({ groupId: groupId, value: value, stateSubFolderName: stateSubFolderName }));
    };

    return (
        <FormControlLabel
            onClick={(event) => event.stopPropagation()}
            onFocus={(event) => event.stopPropagation()}
            control={
                <Checkbox
                    sx={{ margin: 0, padding: '0.25rem' }}
                    checked={selected}
                    indeterminate={indeterminate}
                    onChange={handleCheckboxSelection}
                />
            }
            label={name}
        />
    );
};

export const GroupContent = React.memo(GroupContentMemo);
