import {isEmpty} from "lodash";
import {SimpleAccordion} from "components/SimpleAccordion";
import {Box} from "@mui/material";
import {SimpleTable} from "components/SimpleTable";
import React from "react";

export const HistoryParamsAccordion = ({ params }) => {
    if (isEmpty(params)) return;

    return (
        <SimpleAccordion title={"Parameters:"}>
            <Box sx={{ paddingLeft: '0.5rem', paddingRight: '0.5rem', background: 'rgba(var(--primary), 0.15)' }}>
                <SimpleTable data={params} />
            </Box>
        </SimpleAccordion>
    );
};
