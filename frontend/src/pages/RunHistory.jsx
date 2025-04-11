import React, {useEffect, useState} from 'react';
import {Card, Grid} from "@mui/material";
import Box from "@mui/material/Box";
import {TestRunResultTree} from "../containers/testRunResultTree";
import {TestRunItemCard} from "../containers/testRunItemCard";
import {TestRunStatistic} from "../containers/testRunStatistic";
import {TestRunCarousel} from "../containers/testRunCarousel/testRunCarousel";

const RunHistoryPage = ({match: {params: { folder, testRunId }}}) => {
  const [focusedTest, setFocusedTest] = useState('');

  useEffect(() => {
    setFocusedTest("")
  }, [testRunId]);

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <TestRunCarousel folder={folder} />
      </Grid>
      <Grid item sm={5} xs={12}>
        <Box>
          <TestRunResultTree
            testRunId={testRunId}
            focusedTest={focusedTest}
            setFocusedTest={setFocusedTest}
          />
        </Box>
      </Grid>
      <Grid item sm={7} xs={12}>
        <Box>
          <Card
            sx={{
              paddingLeft: '1.5rem',
              paddingRight: '1.5rem',
              paddingTop: '1rem',
              paddingBottom: '1rem',
              overflowY: 'auto',
              display: 'flex',
              flexDirection: 'column',
              maxHeight: 'calc(100vh - 252px)',
            }}
          >
            {focusedTest ? (
              <TestRunItemCard
                testRunId={testRunId}
                itemId={focusedTest}
                setFocusedTest={setFocusedTest}
              />
            ) : (
              <TestRunStatistic testRunId={testRunId} />
            )}
          </Card>
        </Box>
      </Grid>
    </Grid>
  );
};

export default RunHistoryPage;
