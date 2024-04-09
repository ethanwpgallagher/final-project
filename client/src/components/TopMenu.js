import React from 'react';
import { Link } from 'react-router-dom';
import { styled } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import MenuItem from '@mui/material/MenuItem';

const PREFIX = 'TopMenu';

const Root = styled('div')({
  [`& .${PREFIX}-appBar`]: {
    // Add your AppBar styles here if needed
  },
  [`& .${PREFIX}-title`]: {
    flexGrow: 1,
    '& a': {
        color: 'white',
        textDecoration: 'none'
    },
  },
});

function TopMenu() {
  return (
    <Root>
      <AppBar position="fixed" className={`${PREFIX}-appBar`}>
        <Toolbar>
          <MenuItem>
            <Typography variant="h6" className={`${PREFIX}-title`}>
              <Link to="/">Home</Link>
            </Typography>
          </MenuItem>
          <MenuItem>
            <Typography variant="h6" className={`${PREFIX}-title`}>
              <Link to="/diagnosis">Diagnosis Tool</Link>
            </Typography>
          </MenuItem>
          <MenuItem>
            <Typography variant="h6" className={`${PREFIX}-title`}>
              <Link to="/analysis">Model Analysis</Link>
            </Typography>
          </MenuItem>
          <MenuItem>
            <Typography variant="h6" className={`${PREFIX}-title`}>
              <Link to="/about">About</Link>
            </Typography>
          </MenuItem>
        </Toolbar>
      </AppBar>
    </Root>
  );
}

export default TopMenu;