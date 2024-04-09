import React from 'react';
import TopMenu from '../components/TopMenu';
import HomeContent from '../components/HomeContent';
import Footer from '../components/Footer';
import { styled } from '@mui/material/styles';

const Root = styled('div')({
  display: 'flex',
});

function Home() {
    return (
      <Root>
        <TopMenu />
        <HomeContent />
        <Footer />
      </Root>
    );
}

export default Home;