import React from 'react';
import { render, screen } from '@testing-library/react';
import Analysis from '../pages/Analysis';

jest.mock('../components/TopMenu', () => () => <div data-testid="top-menu">Top Menu</div>);
jest.mock('../components/AnalysisContent', () => () => <div data-testid="analysis-content">Analysis Content</div>);
jest.mock('../components/Footer', () => () => <div data-testid="footer">Footer</div>);

describe('Analysis', () => {
  test('renders all components', () => {
    render(<Analysis />);

    expect(screen.getByTestId('top-menu')).toBeInTheDocument();
    expect(screen.getByTestId('analysis-content')).toBeInTheDocument();
    expect(screen.getByTestId('footer')).toBeInTheDocument();
  });
});
