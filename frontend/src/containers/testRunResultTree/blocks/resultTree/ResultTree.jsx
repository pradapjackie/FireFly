import React from 'react';
import { NestedAccordion } from 'components/NestedAccordion';
import { useTestRunTreeSelector } from '../../slice';
import { GroupContent } from './groupContent';
import { ItemContent } from './itemContent';
import { Card } from '@mui/material';

export const ResultTree = ({ testRunId, focusedTest, setFocusedTest}) => {
  const firstLevel = useTestRunTreeSelector(testRunId, (state) => (state.firstLevel));

  function useGroupInfo(groupId) {
    const name = useTestRunTreeSelector(testRunId, state => state.groups[groupId].name)
    const expanded = useTestRunTreeSelector(testRunId, state => state.groups[groupId].id.split('.').length <= 2)
    const items = useTestRunTreeSelector(testRunId, state => state.groups[groupId].autoTests)
    const groups = useTestRunTreeSelector(testRunId, state => state.groups[groupId].groups)
    return {name, expanded, items, groups}
  }

  const GroupComponent = (props) => {
    return <GroupContent testRunId={testRunId} {...props} />;
  }

  const ItemComponent = (props) => {
    return <ItemContent testRunId={testRunId} {...props} />;
  }

  return (
    <Card
      sx={{
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        maxHeight: 'calc(100vh - 252px)',
      }}
    >
      <NestedAccordion
        firstLevel={firstLevel}
        GroupComponent={GroupComponent}
        ItemComponent={ItemComponent}
        selectedItem={focusedTest}
        itemOnClick={setFocusedTest}
        useGroupInfo={useGroupInfo}
        reverseExpandIcon={true}
        stateSubFolderName={testRunId}
      />
    </Card>
  );
};
