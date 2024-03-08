import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Typography } from '@material-ui/core';

const useStyles = makeStyles(theme => ({
  toolbar: theme.mixins.toolbar,
  title: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
  fullWidth: {
    width: '100%',
  },
}));

function AboutContent() {
    const classes = useStyles();
  
    return (
      <main className={classes.fullWidth}>
        <div className={classes.toolbar} />
        <div className={classes.title}>
          <Typography variant='h6'>About this tool</Typography>
        </div>
        <div className={classes.content}>
          <Typography paragraph>
            Developed by Ethan Gallagher for ECM1234 Individual Project and Literature Review
          </Typography>
        </div>
      </main>
    );
  }
  
  export default AboutContent;