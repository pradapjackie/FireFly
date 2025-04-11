import React, {useEffect} from 'react';
import {isEmpty} from 'lodash';
import {Name} from './blocks/name';
import {Params} from './blocks/params';
import {Description} from './blocks/description';
import {Stages} from './blocks/stages';
import {Button, Box} from '@mui/material';
import RedoIcon from '@mui/icons-material/Redo';
import {useTestRunItemCardSelector, useTestRunItemCardSlice} from "./slice";
import {useDispatch} from "react-redux";
import {ErrorSections} from "./blocks/error";
import {Warnings} from "./blocks/warning";

export const TestRunItemCard = ({testRunId, itemId, setFocusedTest}) => {
  const {actions} = useTestRunItemCardSlice();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(actions.fetch({testRunId, itemId}));
  }, [testRunId, itemId]);

  const {fetchStatus, ...data} = useTestRunItemCardSelector(testRunId, itemId);

  if (fetchStatus !== 'success') {
    return <></>
  }

  return (
    <>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
        }}
      >
        <Name status={data.status} name={`${data.methodName} | ${data.iterationName}`}/>
        <Button
          onClick={() => setFocusedTest('')}
          sx={{
            top: '-15px',
            right: '-25px',
            borderRadius: '0px',
            minWidth: '150px',
          }}
          variant="contained"
          endIcon={<RedoIcon/>}
        >
          View statistic
        </Button>
      </Box>
      {!isEmpty(data.errors) && (
        <ErrorSections errors={data.errors}/>
      )}
      {data.description && <Description description={data.description}/>}
      {data.warnings && <Warnings warnings={data.warnings} />}
      {(!isEmpty(data.params) ||
        !isEmpty(data.envUsed) ||
        !isEmpty(data.generatedParams) ||
        !isEmpty(data.assetsPath) ||
        !isEmpty(data.runConfig)) && (
        <Params
          params={data.params}
          envUsed={data.envUsed}
          generatedParams={data.generatedParams}
          assets={data.assetsPath}
          runConfig={data.runConfig}
        />
      )}
      <Stages stages={data.stages}/>
    </>
  );
}
