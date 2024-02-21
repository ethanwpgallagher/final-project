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

function HomeContent() {
    const classes = useStyles();
  
    return (
      <main className={classes.fullWidth}>
        <div className={classes.toolbar} />
        <div className={classes.title}>
          <Typography variant='h6'>Diabetic Retinopathy Diagnosis Tool and Machine Learning Model Analysis</Typography>
        </div>
        <div className={classes.content}>
          <Typography paragraph>
            Welcome to ...., a Diabetic Retinopathy diagnosis tool to help faciliate diagnosis for DR and consequently diabetes mellitus. 
          </Typography>
        </div>
      </main>
    );
  }
  
  export default HomeContent;