import React from 'react';
import TopMenu from '../components/TopMenu';
import DiagnosisContent from '../components/DiagnosisContent';
import Footer from '../components/Footer';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
    root: {
      display: 'flex',
    },
  }));

function Diagnosis() {
    const classes = useStyles();
  
    return (
      <div className={classes.root}>
        <TopMenu />
        <DiagnosisContent />
        <Footer />
      </div>
    );
  }
  
  export default Diagnosis;