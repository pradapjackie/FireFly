import React from 'react';
import {Group} from "./group"


export function NestedAccordion({
                                  firstLevel,
                                  GroupComponent,
                                  ItemComponent,
                                  selectedItem,
                                  itemOnClick,
                                  reverseExpandIcon,
                                  useGroupInfo,
                                  stateSubFolderName
                                }) {

  const firstLevelSorted = [...firstLevel].sort()
  return (<>
    {firstLevelSorted.map((groupId) => <Group
      key={groupId}
      groupId={groupId}
      nested={false}
      GroupComponent={GroupComponent}
      ItemComponent={ItemComponent}
      selectedItem={selectedItem}
      itemOnClick={itemOnClick}
      reverseExpandIcon={reverseExpandIcon}
      useGroupInfo={useGroupInfo}
      stateSubFolderName={stateSubFolderName}
    />)}
  </>);
}
