import React from 'react';
import TopMenu from '../components/TopMenu';
import AboutContent from '../components/AboutContent';
import Footer from '../components/Footer';
import { styled } from '@mui/material/styles';

const Root = styled('div')({
  display: 'flex',
});

function About() {
    return (
      <Root>
        <TopMenu />
        <AboutContent />
        <Footer />
      </Root>
    );
}

export default About;