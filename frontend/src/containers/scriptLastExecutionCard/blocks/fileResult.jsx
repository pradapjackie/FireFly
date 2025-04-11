import React, { useState } from 'react';
import { Card, CardMedia, CardContent, IconButton, CardActionArea } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import Box from '@mui/material/Box';

const FileCard = ({ data: { title, url, type } }) => {
    const [hover, setHover] = useState(false);

    const handleDownload = (event) => {
        event.stopPropagation();
        const link = document.createElement('a');
        link.href = url;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <Card
            sx={{ width: 125, position: 'relative', cursor: 'pointer', textAlign: 'center' }}
            onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}
        >
            <CardActionArea component="div">
                <CardMedia
                    component="img"
                    image={`/assets/images/file-types/${type}.svg`}
                    sx={{ padding: '1rem', filter: 'brightness(90%)' }}
                />

                {hover && (
                    <IconButton
                        onClick={handleDownload}
                        sx={{
                            position: 'absolute',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                            color: 'white',
                            backgroundColor: 'rgba(0, 0, 0, 0.4)',
                            '&:hover': {
                                backgroundColor: 'rgba(0, 0, 0, 0.6)',
                            },
                        }}
                    >
                        <DownloadIcon fontSize="large" />
                    </IconButton>
                )}

                <CardContent sx={{ padding: '0.5rem !important' }}>
                    <Box component="h5" sx={{ margin: 0 }}>
                        {title}
                    </Box>
                </CardContent>
            </CardActionArea>
        </Card>
    );
};

export const FileResult = ({ data }) => {
    return (
        <Box sx={{ padding: '0.5rem', background: 'rgba(var(--primary), 0.15)' }}>
            <FileCard data={data} />
        </Box>
    );
};

export const FilesResult = ({ data }) => {
    return (
        <Box sx={{ padding: '0.5rem', background: 'rgba(var(--primary), 0.15)', display: 'flex', gap: '10px'}}>
            {Object.values(data).map((item, i) => (
                <FileCard key={i} data={item.object} />
            ))}
        </Box>
    );
};
