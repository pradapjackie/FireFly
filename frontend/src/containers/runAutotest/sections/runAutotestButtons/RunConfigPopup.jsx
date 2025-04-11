import React from 'react';
import { Dialog, DialogContent, DialogTitle } from '@mui/material';
import { DynamicForm } from 'components/DynamicForm';

export const RunConfigPopupMemo = ({
    isOpen,
    setOpen,
    requiredRunConfig,
    runConfig,
    setRunConfig,
    fetchDynamicData,
}) => {
    return (
        <Dialog open={isOpen} onClose={() => setOpen(false)} maxWidth="sm" fullWidth={true}>
            <DialogTitle>Config</DialogTitle>
            <DialogContent dividers={true}>
                <DynamicForm
                    requiredConfig={requiredRunConfig}
                    resultConfig={runConfig}
                    setResultConfig={setRunConfig}
                    fetchDynamicData={fetchDynamicData}
                />
            </DialogContent>
        </Dialog>
    );
};

export const RunConfigPopup = React.memo(RunConfigPopupMemo);
