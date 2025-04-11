import React, { useEffect } from 'react';
import { NestedAccordion } from 'components/NestedAccordion';
import { useDispatch } from 'react-redux';
import { actions, useRunAutotestSliceSelector } from '../../slice';
import { GroupContent } from './blocks/groupContent';
import { ItemContent } from './blocks/itemContent';
import { Card } from '@mui/material';

export const SelectTestsTreeMemo = ({ folder }) => {
    const dispatch = useDispatch();
    const firstLevel = useRunAutotestSliceSelector(folder, (state) => state.groups.firstLevel);

    const handleTestFocus = (itemId) => {
        dispatch(actions.testFocused({ testId: itemId, folder: folder }));
    };

    useEffect(() => {
        return () => handleTestFocus('');
    }, []);

    function useGroupInfo(groupId) {
        return useRunAutotestSliceSelector(folder, (state) => state.groups.entities[groupId]);
    }

    return (
        <Card
            sx={{
                paddingTop: '1rem',
                overflowY: 'auto',
                display: 'flex',
                flexDirection: 'column',
                maxHeight: 'calc(100vh - 290px)',
            }}
        >
            <NestedAccordion
                firstLevel={firstLevel}
                GroupComponent={GroupContent}
                ItemComponent={ItemContent}
                itemOnClick={handleTestFocus}
                useGroupInfo={useGroupInfo}
                reverseExpandIcon={false}
                stateSubFolderName={folder}
            />
        </Card>
    );
};

export const SelectTestsTree = React.memo(SelectTestsTreeMemo);
