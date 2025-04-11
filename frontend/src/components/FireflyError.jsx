import React, {useEffect, useRef, useState} from "react";
import {Accordion, AccordionDetails, AccordionSummary, Box, Divider} from "@mui/material";
import Typography from "@mui/material/Typography";

export const FireFlyError = ({ errorName, errorMessage, errorTrace }) => {
  const ref = useRef(null);
  const [blur, setBlur] = useState(true);
  const [height, setHeight] = useState(0);

  useEffect(() => {
    if (ref.current && ref.current.clientHeight) {
      setHeight(ref.current.clientHeight);
    }
  });

  return (
    <Box ref={ref} sx={{paddingBottom: '1rem'}}>
      <Box
        sx={[
          blur &&
            height >= 300 && {
              maxHeight: 300,
              position: 'relative',
              overflow: 'hidden',
              '&::after': {
                content: '""',
                position: 'absolute',
                left: '0px',
                right: '0px',
                height: '20%',
                bottom: '0px',
                background: `linear-gradient(180deg, rgba(26,32,56,0.15) 30%, rgba(34,42,69,1) 100%);`,
              },
            },
        ]}
        onClick={() => {
          setBlur(false);
        }}
      >
        <Box
          sx={{
            whiteSpace: 'pre-wrap',
            padding: '0.5rem',
            backgroundColor: 'rgba(var(--primary), 0.15)',
          }}
        >
          <Typography
            sx={{
              paddingBottom: '0.5rem',
              fontWeight: '700',
              color: 'error.main',
            }}
            variant={'subtitle1'}
          >
            {errorName}
          </Typography>
          {errorMessage}
        </Box>
      </Box>
      <Divider />
      {errorTrace && (
        <Accordion
          square={true}
          sx={{ backgroundColor: 'rgba(var(--primary), 0.15)' }}
        >
          <AccordionSummary>Traceback:</AccordionSummary>
          <AccordionDetails>
            <Box sx={{ whiteSpace: 'pre-wrap' }}>{errorTrace}</Box>
          </AccordionDetails>
        </Accordion>
      )}
    </Box>
  );
};
