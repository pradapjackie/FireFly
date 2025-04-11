import React, { useState, useEffect } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import AutoHeight from 'embla-carousel-auto-height';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import { Divider } from '@mui/material';
import { SimpleTable } from 'components/SimpleTable';
import { isEmpty } from 'lodash';
import { Assets } from './assets';

const SwipeableViews = ({ children, emblaRef }) => {
    return (
        <Box className="embla">
            <Box className="embla__viewport" ref={emblaRef} sx={{overflow: 'hidden'}}>
                <Box
                    className="embla__container"
                    sx={{ transition: 'height 0.2s', display: 'flex', alignItems: 'flex-start' }}
                >
                    {children}
                </Box>
            </Box>
        </Box>
    );
};

const SwipeTab = ({ index, children }) => {
    return (
        <Box
            sx={{ paddingTop: '1rem', flexGrow: 0, flexShrink: 0, flexBasis: '100%' }}
            className="embla__slide"
            key={index}
        >
            <Box className="embla__slide__number">{children}</Box>
        </Box>
    );
};

const ParamsTabs = ({ columns, params, envUsed, generatedParams, assets, runConfig }) => {
    const [value, setValue] = useState(0);
    const [emblaRef, emblaApi] = useEmblaCarousel({}, [AutoHeight()]);

    useEffect(() => {
        if (emblaApi) emblaApi.scrollTo(value);
    }, [emblaApi, value]);

    const tabs = [];

    if (columns.includes('parameters')) {
        const parametersIndex = columns.indexOf('parameters');
        tabs.push(
            <SwipeTab key={parametersIndex} index={parametersIndex}>
                <SimpleTable name={'parameters'} data={params} />
            </SwipeTab>,
        );
    }
    if (columns.includes('run config')) {
        const runConfigIndex = columns.indexOf('run config');
        tabs.push(
            <SwipeTab key={runConfigIndex} index={runConfigIndex}>
                <SimpleTable name={'run config'} data={runConfig} />
            </SwipeTab>,
        );
    }
    if (columns.includes('environment used')) {
        const envIndex = columns.indexOf('environment used');
        tabs.push(
            <SwipeTab key={envIndex} index={envIndex}>
                <SimpleTable name={'environment used'} data={envUsed} />
            </SwipeTab>,
        );
    }
    if (columns.includes('generated params')) {
        const generatedParamsIndex = columns.indexOf('generated params');
        tabs.push(
            <SwipeTab key={generatedParamsIndex} index={generatedParamsIndex}>
                <SimpleTable name={'generated params'} data={generatedParams} />
            </SwipeTab>,
        );
    }
    if (columns.includes('assets')) {
        const assetsIndex = columns.indexOf('assets');
        tabs.push(
            <SwipeTab key={assetsIndex} index={assetsIndex}>
                <Assets name={'assets'} data={assets} />
            </SwipeTab>,
        );
    }

    return (
        <Box sx={{ marginTop: '0.5rem', color: 'rgba(255, 255, 255, 1)' }}>
            <Tabs
                value={value}
                onChange={(event, newValue) => {
                    setValue(newValue);
                }}
                indicatorColor="primary"
                textColor="inherit"
                variant="fullWidth"
            >
                {columns.map((item, ind) => (
                    <Tab sx={{ fontSize: '1rem', textTransform: 'capitalize' }} value={ind} label={item} key={ind} />
                ))}
            </Tabs>
            <Divider sx={{ marginBottom: '0.25rem' }} />
            <SwipeableViews emblaRef={emblaRef}>{tabs}</SwipeableViews>
        </Box>
    );
};

export const Params = ({ params, envUsed, generatedParams, assets, runConfig }) => {
    const columns = ['parameters', 'environment used', 'generated params'];
    !isEmpty(runConfig) && columns.splice(1, 0, 'run config');
    !isEmpty(assets) && columns.push('assets');

    return (
        <ParamsTabs
            columns={columns}
            params={params}
            envUsed={envUsed}
            generatedParams={generatedParams}
            assets={assets}
            runConfig={runConfig}
        />
    );
};
