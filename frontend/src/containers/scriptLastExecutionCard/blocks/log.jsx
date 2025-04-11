import React, { useRef, useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import { DotLoading } from 'components/Loading/DotLoading';
import Typography from '@mui/material/Typography';
import Scrollbar from 'react-perfect-scrollbar';
import { isEmpty } from 'lodash';
import { SimpleAccordion } from 'components/SimpleAccordion';
import { useScriptLastExecutionCardSelector } from '../slice';

export const LogPanel = ({ log, disableAutoScroll = false, status = 'done' }) => {
    const scrollRef = useRef();
    const [scrolledByUser, SetScrolledByUser] = useState(disableAutoScroll);

    useEffect(() => {
        if (scrollRef?.current && !scrolledByUser) {
            scrollRef.current.scrollTop = Number.MAX_SAFE_INTEGER;
        }
    }, [log, scrolledByUser]);

    const handleUserScroll = () => {
        if (Object.keys(log).length > 0) {
            SetScrolledByUser(true);
        }
    };

    return (
        <Scrollbar
            containerRef={(el) => (scrollRef.current = el)}
            style={{ maxHeight: '30vh', position: 'relative', background: '#111', color: '#fff' }}
            onScrollUp={() => handleUserScroll()}
            onScrollLeft={() => handleUserScroll()}
            onScrollRight={() => handleUserScroll()}
        >
            <Box>
                <Box
                    sx={{
                        display: 'flex',
                        whiteSpace: 'pre',
                    }}
                >
                    <Box component="code" sx={{ marginRight: '0.5rem', marginLeft: '0.5rem' }}>
                        {Object.keys(log).map((index) => (
                            <Box component="span" key={index} sx={{ marginTop: '0.5rem', marginBottom: '0.5rem' }}>
                                {index}
                                {'\n'}
                            </Box>
                        ))}
                    </Box>
                    <Box component="code">
                        {Object.entries(log).map(([index, logLine]) => (
                            <Box component="span" key={index}>
                                {logLine}
                                {'\n'}
                            </Box>
                        ))}
                    </Box>
                </Box>
                {status === 'pending' && (
                    <Box sx={{ padding: '1rem', marginLeft: '2rem' }}>
                        <DotLoading />
                    </Box>
                )}
            </Box>
        </Scrollbar>
    );
};

export const Log = ({ status, scriptId }) => {
    const log = useScriptLastExecutionCardSelector(scriptId, (state) => state.log);

    if (status === 'idle') {
        return (
            <Typography sx={{ paddingTop: '1rem' }} variant={'subtitle1'}>
                The script has never been executed
            </Typography>
        );
    }

    if (isEmpty(log)) return;

    return (
        <Box sx={{ paddingTop: '1rem' }}>
            <Typography sx={{ paddingBottom: '0.5rem', fontWeight: '700' }} variant={'subtitle1'}>
                Log:
            </Typography>
            <LogPanel log={log} status={status} />
        </Box>
    );
};

export const LogAccordion = ({ log }) => {
    if (isEmpty(log)) return;

    return (
        <SimpleAccordion title={'Log:'}>
            <LogPanel log={log} disableAutoScroll={true} />
        </SimpleAccordion>
    );
};
