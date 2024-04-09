import React from 'react';
import { styled } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Typography from '@mui/material/Typography';

const PREFIX = 'Footer';

const StyledAppBar = styled(AppBar)({
  [`&.${PREFIX}-appBar`]: {
    top: 'auto',
    bottom: 0,
  },
  [`& .${PREFIX}-title`]: {
    flexGrow: 1,
    marginLeft: 10,
  },
  [`& .${PREFIX}-footer`]: {
    marginLeft: 20,
    fontSize: 17,
  },
});

function Footer() {
    return (
        <StyledAppBar position='fixed' className={`${PREFIX}-appBar`}>
            <Typography variant='h6' className={`${PREFIX}-footer`}>
                © Copyright 2024
            </Typography>
        </StyledAppBar>
    );
}

export default Footer;