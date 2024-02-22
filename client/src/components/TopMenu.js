import React from 'react';
import { Link } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { MenuItem } from '@material-ui/core';

const useStyles = makeStyles(theme => ({
  appBar: {
    // your styles here
  },
  title: {
    flexGrow: 1,
    '& a': {
        color: 'white',
        textDecoration: 'none'
    },
  },
}));

function TopMenu() {
  const classes = useStyles();

  return (
    <AppBar position='fixed' className={classes.appBar}>
      <Toolbar>
        <MenuItem>
          <Typography variant='h6' className={classes.title}>
            <Link to="/">Home</Link>
          </Typography>
        </MenuItem>
        <MenuItem>
          <Typography variant='h6' className={classes.title}>
            <Link to="/diagnosis">Diagnosis Tool</Link>
          </Typography>
        </MenuItem>
        <MenuItem>
          <Typography variant='h6' className={classes.title}>
            <Link to="/analysis">Model Analysis</Link>
          </Typography>
        </MenuItem>
        <MenuItem>
          <Typography variant='h6' className={classes.title}>
            <Link to="/about">About</Link>
          </Typography>
        </MenuItem>
      </Toolbar>
    </AppBar>
  );
}

export default TopMenu;
