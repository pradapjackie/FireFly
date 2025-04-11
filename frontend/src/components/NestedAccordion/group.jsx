import React, {useState} from 'react';

import {Accordion, AccordionSummary, AccordionDetails} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import {Item} from "./item"


export function GroupMemo({
                            groupId,
                            nested,
                            GroupComponent,
                            ItemComponent,
                            selectedItem,
                            itemOnClick,
                            useGroupInfo,
                            reverseExpandIcon,
                            stateSubFolderName
                          }) {
  const {name, expanded, items, groups} = useGroupInfo(groupId)
  const sortedGroups = [...groups].sort()
  const sortedItems = [...items].sort()
  const [groupExpanded, setGroupExpanded] = useState(expanded)
  const handleGroupExpanded = () => {
    setGroupExpanded(!groupExpanded);
  };

  const groupsList = sortedGroups ? sortedGroups.map((groupID) => <Group
    key={groupID}
    groupId={groupID}
    nested={true}
    GroupComponent={GroupComponent}
    ItemComponent={ItemComponent}
    selectedItem={selectedItem}
    itemOnClick={itemOnClick}
    useGroupInfo={useGroupInfo}
    reverseExpandIcon={reverseExpandIcon}
    stateSubFolderName={stateSubFolderName}
  />) : <></>;

  const itemsList = sortedItems ? sortedItems.map((itemId) => <Item
    key={itemId}
    itemId={itemId}
    focused={itemId === selectedItem}
    ItemComponent={ItemComponent}
    onClick={itemOnClick}
    stateSubFolderName={stateSubFolderName}
  />) : <></>;

  return (<Accordion
    TransitionProps={{unmountOnExit: true}}
    square={true}
    expanded={groupExpanded}
    onChange={handleGroupExpanded}
    disableGutters={true}
    key={name}
    sx={[nested && {paddingLeft: '16px'}]}
  >
    <AccordionSummary
      expandIcon={<ExpandMoreIcon/>}
      aria-label={name}
      id={name}
      sx={[
        {
          padding: '0px 16px 0px 16px',
          minHeight: 'auto !important',
          backgroundColor: 'transparent',
          borderTopLeftRadius: '3px',
          borderTopRightRadius: '3px',
          '&:hover': {
            backgroundColor: 'action.hover',
          },
          '& .MuiAccordionSummary-content': {
            justifyContent: 'space-between',
            alignItems: 'center',
            margin: '0 !important',
          },
          '& .MuiAccordionSummary-expandIconWrapper': {
            padding: '4px !important',
            margin: '0px !important',
            height: 'auto !important',
            fontSize: 'auto !important',
          }
        },
        reverseExpandIcon && {flexDirection: 'row-reverse'}
      ]}
    >
      <GroupComponent groupId={groupId} stateSubFolderName={stateSubFolderName}/>
    </AccordionSummary>
    <AccordionDetails
      sx={{
        display: 'flex',
        flexDirection: 'column',
        padding: '0px',
      }}
    >
      {groupsList}
      {itemsList}
    </AccordionDetails>
  </Accordion>);
}

export const Group = React.memo(GroupMemo);
