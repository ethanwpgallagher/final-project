import React from 'react';
import { styled } from '@mui/material/styles';
import { Typography } from '@mui/material';

const PREFIX = 'HomeContent';

const Root = styled('main')(({ theme }) => ({
  [`&.${PREFIX}-fullWidth`]: {
    width: '100%',
  },
  [`& .${PREFIX}-toolbar`]: theme.mixins.toolbar,
  [`& .${PREFIX}-title`]: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
  },
  [`& .${PREFIX}-content`]: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
}));

function HomeContent() {
    return (
      <Root className={`${PREFIX}-fullWidth`}>
        <div className={`${PREFIX}-toolbar`} />
        <div className={`${PREFIX}-title`}>
          <Typography variant='h6'>Diabetic Retinopathy Diagnosis Tool and Machine Learning Model Analysis</Typography>
        </div>
        <div className={`${PREFIX}-content`}>
          <Typography paragraph>
            Welcome to ...., a Diabetic Retinopathy diagnosis tool to help facilitate diagnosis for DR and consequently diabetes mellitus.
          </Typography>
        </div>
      </Root>
    );
}

export default HomeContent;