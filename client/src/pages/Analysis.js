import React from 'react';
import TopMenu from '../components/TopMenu';
import AnalysisContent from '../components/AnalysisContent';
import Footer from '../components/Footer';
import { styled } from '@mui/material/styles';

const Root = styled('div')({
  display: 'flex',
});

function Analysis() {
    return (
      <Root>
        <TopMenu />
        <AnalysisContent />
        <Footer />
      </Root>
    );
}

export default Analysis;
