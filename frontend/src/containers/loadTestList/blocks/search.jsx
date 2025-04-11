import React from 'react';
import { InputAdornment, TextField } from '@mui/material';
import FilterListIcon from '@mui/icons-material/FilterList';

export const LoadTestSearch = ({ search, setSearch, disabled }) => {
    return (
        <TextField
            label="Load test search"
            disabled={disabled}
            variant="standard"
            sx={{ width: '100%', marginBottom: '1rem' }}
            color="secondary"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            InputProps={{
                startAdornment: (
                    <InputAdornment position="start">
                        <FilterListIcon sx={[disabled && { color: 'rgba(255, 255, 255, 0.5)' }]} />
                    </InputAdornment>
                ),
            }}
        />
    );
};
