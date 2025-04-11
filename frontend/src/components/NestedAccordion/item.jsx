import React from 'react';
import {Accordion, AccordionSummary} from '@mui/material';

export function Item({itemId, ItemComponent, focused, onClick, stateSubFolderName}) {
  return (<Accordion
      TransitionProps={{unmountOnExit: true}}
      disableGutters={true}
      square={true}
      key={itemId}
      sx={{
        width: '100%', paddingLeft: '16px', boxShadow: 'none', '&:before': {
          display: 'none !important',
        },
      }}
      onChange={() => onClick(itemId)}
    >
      <AccordionSummary
        sx={[{
          padding: '0px 24px',
          minHeight: 'auto !important',
          backgroundColor: 'transparent',
          borderTopLeftRadius: '3px',
          borderTopRightRadius: '3px',
          '&:hover': {
            backgroundColor: 'action.hover',
          },
          height: '36px',
          '& .MuiAccordionSummary-content': {
            width: '100%',
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            margin: '0 !important',
          },
          '& .MuiAccordionSummary-expandIconWrapper': {
            padding: '6px !important', margin: '0px !important', height: 'auto !important', fontSize: 'auto !important',
          },
        }, focused && {backgroundColor: 'action.selected'}]}
      >
        <ItemComponent itemId={itemId} stateSubFolderName={stateSubFolderName}/>
      </AccordionSummary>
    </Accordion>);
}
