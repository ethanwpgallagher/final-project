import React from 'react';
import TopMenu from '../components/TopMenu';
import AboutContent from '../components/AboutContent';
import Footer from '../components/Footer';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
      display: 'flex',
    },
  }));

function About() {
    const classes = useStyles();
  
    return (
      <div className={classes.root}>
        <TopMenu />
        <AboutContent />
        <Footer />
      </div>
    );
  }
  
  export default About;