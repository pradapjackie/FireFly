import React from 'react';
import { Box, Card } from '@mui/material';
import { SmallStatusChip } from 'components/StatusChip';
import { SimpleTable } from 'components/SimpleTable';
import { format } from 'date-fns';
import { ScriptResultAccordion } from '../../scriptLastExecutionCard/blocks/result';
import { ErrorSectionAccordion } from '../../scriptLastExecutionCard/blocks/errors';
import { LogAccordion } from '../../scriptLastExecutionCard/blocks/log';
import { EnvUsedAccordion } from '../../scriptLastExecutionCard/blocks/envUsed';
import {HistoryParamsAccordion} from "../../scriptLastExecutionCard/blocks/params";

export const ListHistoryCard = ({ historyItem }) => {
    return (
        <Card
            sx={{
                padding: '1rem',
                marginBottom: '1rem',
                display: 'flex',
                flexWrap: 'wrap',
                justifyContent: 'space-between',
                alignItems: 'center',
                minHeight: 'auto !important',
            }}
        >
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'row',
                    width: '100%'
                }}
            >
                <Box sx={{ width: '60%', paddingRight: '2rem' }}>
                    <ScriptResultAccordion result={historyItem.result} />
                    <ErrorSectionAccordion errors={historyItem.errors} />
                    <LogAccordion log={historyItem.log} />
                    <HistoryParamsAccordion params={historyItem.params} />
                    <EnvUsedAccordion envUsed={historyItem.envUsed} />
                </Box>
                <Box sx={{ width: '40%' }}>
                    <SimpleTable
                        data={{
                            Status: <SmallStatusChip status={historyItem.status} />,
                            User: historyItem.userName,
                            Env: historyItem.environment,
                            Start: format(new Date(historyItem.startTime), 'dd.MM.yyyy HH:mm'),
                            End: format(new Date(historyItem.endTime), 'dd.MM.yyyy HH:mm'),
                        }}
                        stringify={false}
                    />
                </Box>
            </Box>
        </Card>
    );
};
