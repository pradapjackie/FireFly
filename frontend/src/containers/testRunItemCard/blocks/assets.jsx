import React from 'react';
import {Card, Grid} from "@mui/material";
import {AssetCard} from "./assetsCard";


const AssetsMemo = ({data}) => {
  return (
    <Card sx={{backgroundColor: 'background.default', padding: '0.5rem'}}>
      <Grid container spacing={2}>
        {
          Object.values(data).map((item, i) =>
            <Grid key={i} item xs={4}>
              <AssetCard type={item.type} title={item.title} url={item.url}/>
            </Grid>
          )
        }
      </Grid>
    </Card>
  );
};

export const Assets = React.memo(AssetsMemo);
