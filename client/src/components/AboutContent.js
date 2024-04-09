import React from 'react';
import { styled } from '@mui/material/styles';
import { Typography } from '@mui/material';

const PREFIX = 'AboutContent';

const Root = styled('main', {
  shouldForwardProp: (prop) => prop !== 'className' && prop !== `${PREFIX}-fullWidth` && prop !== `${PREFIX}-toolbar` && prop !== `${PREFIX}-title` && prop !== `${PREFIX}-content`,
})(({ theme }) => ({
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

function AboutContent() {
  return (
    <Root className={`${PREFIX}-fullWidth`}>
      <div className={`${PREFIX}-toolbar`} />
      <div className={`${PREFIX}-title`}>
        <Typography variant='h6'>About this tool</Typography>
      </div>
      <div className={`${PREFIX}-content`}>
        <Typography paragraph>
          Developed by Ethan Gallagher for ECM1234 Individual Project and Literature Review
        </Typography>
      </div>
    </Root>
  );
}

export default AboutContent;
