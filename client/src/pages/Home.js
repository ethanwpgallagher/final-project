import React from 'react';
import TopMenu from '../components/TopMenu';
import HomeContent from '../components/HomeContent';
import Footer from '../components/Footer';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
      display: 'flex',
    },
  }));

function Home() {
    const classes = useStyles();
  
    return (
      <div className={classes.root}>
        <TopMenu />
        <HomeContent />
        <Footer />
      </div>
    );
  }
  
  export default Home;