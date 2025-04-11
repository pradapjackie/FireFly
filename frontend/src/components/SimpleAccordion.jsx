import { Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import React from 'react';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

export const SimpleAccordion = ({ title, children }) => {
    return (
        <Accordion
            TransitionProps={{ unmountOnExit: true }}
            square={true}
            disableGutters={true}
            key={title}
            sx={{
                width: '100%',
                backgroundColor: 'transparent',
                boxShadow: 'none',
                '&:before': {
                    display: 'none',
                },
            }}
        >
            <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                id={name}
                sx={[
                    {
                        padding: '0px',
                        minHeight: 'auto',
                        flexDirection: 'row-reverse',
                        '& .MuiAccordionSummary-content': {
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            margin: '0 !important',
                        },
                        '& .MuiAccordionSummary-expandIconWrapper': {
                            padding: '4px',
                            margin: '0px',
                            height: 'auto',
                            fontSize: 'auto',
                        },
                    },
                ]}
            >
                {title}
            </AccordionSummary>
            <AccordionDetails
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    padding: '0px',
                }}
            >
                {children}
            </AccordionDetails>
        </Accordion>
    );
};
