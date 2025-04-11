import React, { useEffect, useRef, useState } from 'react';
import { Card, Box } from '@mui/material';
import { OneRunCard } from './oneRunCard';
import { CarouselProvider, Slider, Slide } from 'pure-react-carousel';
import 'pure-react-carousel/dist/react-carousel.es.css';
import { useTestRunCarouselSlice, useTestRunCarouselSliceSelector } from './slice';
import { useDispatch } from 'react-redux';
import { useEnvSliceSelector } from '../enviroment/slice';

export const TestRunCarousel = ({ folder }) => {
    const { actions } = useTestRunCarouselSlice();
    const dispatch = useDispatch();

    const ids = useTestRunCarouselSliceSelector(folder, (state) => state.ids);
    const status = useTestRunCarouselSliceSelector(folder, (state) => state.status);
    const env = useEnvSliceSelector((state) => state.selected);

    const carouselRef = useRef(null);
    const slideRef = useRef(null);
    const [visibleSlides, setVisibleSlides] = useState(0);

    const isSuccess = status === 'success';

    useEffect(() => {
        if (folder && env) dispatch(actions.fetch({ folder: folder, env: env }));
    }, [folder, env]);

    useEffect(() => {
        const carouselWidth = carouselRef.current ? carouselRef.current.offsetWidth : 0;
        const slideWidth = slideRef.current ? slideRef.current.offsetWidth : 0;
        const maxVisibleSlides = slideWidth ? carouselWidth / slideWidth : 0;
        setVisibleSlides(maxVisibleSlides);
    }, [carouselRef.current, slideRef.current, ids.length]);

    const slides = ids.map((id) => (
        <Slide key={id} index={id}>
            <div ref={slideRef}>
                <OneRunCard id={id} folder={folder} />
            </div>
        </Slide>
    ));

    return (
        <>
            {isSuccess ? (
                <div ref={carouselRef}>
                    <Card sx={{ padding: '0.75rem' }}>
                        <Box sx={{ width: '100%' }}>
                            <CarouselProvider
                                naturalSlideWidth={200}
                                naturalSlideHeight={80}
                                totalSlides={ids.length}
                                visibleSlides={visibleSlides}
                                isIntrinsicHeight={true}
                            >
                                <Slider>{slides}</Slider>
                            </CarouselProvider>
                        </Box>
                    </Card>
                </div>
            ) : (
                <></>
            )}
        </>
    );
};
