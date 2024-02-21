import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { MenuItem } from '@material-ui/core';

const useStyles = makeStyles(theme => ({
  appBar: {
  title: {
    flexGrow: 1
  }
}
}));

function TopMenu() {
    const classes = useStyles();

    return (
        <AppBar position='fixed' className={classes.appBar}>
            <Toolbar>
                <MenuItem>
                    <Typography variant='h6' className={classes.title}>
                        Home
                    </Typography>
                </MenuItem>
                <MenuItem>
                    <Typography variant='h6' className={classes.title}>
                        Diagnosis Tool
                    </Typography>
                </MenuItem>
                <MenuItem>
                    <Typography variant='h6' className={classes.title}>
                        Model Analysis
                    </Typography>
                </MenuItem>
                <MenuItem>
                    <Typography variant='h6' className={classes.title}>
                        About
                    </Typography>
                </MenuItem>
            </Toolbar>
        </AppBar>
    );
}

export default TopMenu;