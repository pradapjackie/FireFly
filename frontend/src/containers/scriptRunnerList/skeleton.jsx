import React from 'react';
import { Skeleton } from '@mui/material';

export const ScriptListSkeleton = () => {
    return (
        <>
            {Array(10).fill(0).map((_, index) => (
                <Skeleton
                    key={index}
                    animation="wave"
                    variant="rectangular"
                    height="50px"
                    width="100%"
                    sx={{
                        marginBottom: '1rem',
                        borderRadius: '5px',
                    }}
                />
            ))}
        </>
    );
};
