import React, { useEffect, useRef } from 'react';
import { Box, Card } from '@mui/material';

export const LoadTestCard = ({ loadTestId, name, description, isFocused, setFocused }) => {
    const ref = useRef(null);

    useEffect(() => {
        if (isFocused && ref.current) {
            const top = ref.current.getBoundingClientRect().top;
            const needToScroll = top + 50 >= window.innerHeight;
            if (needToScroll) {
                ref.current.scrollIntoView();
            }
        }
    }, [ref, isFocused]);

    return (
        <Card
            ref={ref}
            sx={[
                {
                    padding: '1rem',
                    marginBottom: '1rem',
                    display: 'flex',
                    flexWrap: 'wrap',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    minHeight: 'auto !important',
                },
                isFocused && { backgroundColor: 'action.selected' },
                !isFocused && {
                    '&:hover': {
                        backgroundColor: 'action.hover',
                    },
                },
            ]}
            onClick={() => setFocused(loadTestId)}
        >
            <Box
                sx={{
                    marginLeft: '0.5rem',
                }}
            >
                <Box component="h5" sx={{ margin: 0 }}>
                    {name}
                </Box>
                {description && (
                    <Box
                        component="p"
                        sx={{
                            marginBottom: 0,
                            marginTop: '0.5rem',
                            color: 'text.secondary',
                            fontWeight: 'normal',
                        }}
                    >
                        {description}
                    </Box>
                )}
            </Box>
            <span ref={ref} />
        </Card>
    );
};
