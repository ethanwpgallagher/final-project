import React from 'react';
import TopMenu from '../components/TopMenu';
import AnalysisContent from '../components/AnalysisContent';
import Footer from '../components/Footer';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
    root: {
      display: 'flex',
    },
  }));

function Analysis() {
    const classes = useStyles();
  
    return (
      <div className={classes.root}>
        <TopMenu />
        <AnalysisContent />
        <Footer />
      </div>
    );
  }
  
  export default Analysis;