import React from 'react';
import { render, screen } from '@testing-library/react';
import About from '../pages/About';

// Mock necessary components for the About page
jest.mock('../components/TopMenu', () => () => <div data-testid="top-menu">Top Menu</div>);
jest.mock('../components/AboutContent', () => () => <div data-testid="about-content">About Content</div>);
jest.mock('../components/Footer', () => () => <div data-testid="footer">Footer</div>);

describe('About', () => {
  test('renders all components', () => {
    // checks if the About page renders its components
    render(<About />);

    // checks if the mocked components appear
    expect(screen.getByTestId('top-menu')).toBeInTheDocument();
    expect(screen.getByTestId('about-content')).toBeInTheDocument();
    expect(screen.getByTestId('footer')).toBeInTheDocument();
  });
});
