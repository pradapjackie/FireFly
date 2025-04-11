import React, {useEffect} from "react";
import {useDispatch} from "react-redux";
import {useTestRunTreeSlice, useTestRunTreeSelector} from "./slice";
import {TestResultTreeSkeleton} from "./blocks/skeleton";
import {Card} from "@mui/material";
import {IdleStub} from "./blocks/idleStub";
import {ResultTree} from "./blocks/resultTree/ResultTree";
import {FailedStub} from "./blocks/failedStub";

export const TestRunResultTree = ({testRunId, focusedTest, setFocusedTest}) => {
  const { actions } = useTestRunTreeSlice();
  const dispatch = useDispatch();
  const fetchStatus = useTestRunTreeSelector(testRunId, state => state.fetchStatus)
  const status = useTestRunTreeSelector(testRunId, state => state.status)

  useEffect(() => {
    dispatch(actions.fetch({ testRunId }));
  }, [testRunId]);

  let component

  if (fetchStatus !== 'success') {
    component = <TestResultTreeSkeleton/>
  } else if (status === 'idle') {
    component = <IdleStub/>
  } else if (status === 'failed') {
    component = <FailedStub/>
  } else {
    component = <ResultTree testRunId={testRunId} focusedTest={focusedTest} setFocusedTest={setFocusedTest} />;
  }

  return (
    <Card
      sx={{
        paddingTop: '1rem',
        overflowY: "auto",
        display: "flex",
        flexDirection: "column",
        maxHeight: "calc(100vh - 252px)"
      }}
    >
      {component}
    </Card>
  )
}
