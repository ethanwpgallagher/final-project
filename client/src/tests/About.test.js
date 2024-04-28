import React from 'react';
import { render, screen } from '@testing-library/react';
import About from '../pages/About';

jest.mock('../components/TopMenu', () => () => <div data-testid="top-menu">Top Menu</div>);
jest.mock('../components/AboutContent', () => () => <div data-testid="about-content">About Content</div>);
jest.mock('../components/Footer', () => () => <div data-testid="footer">Footer</div>);

describe('About', () => {
  test('renders all components', () => {
    render(<About />);

    expect(screen.getByTestId('top-menu')).toBeInTheDocument();
    expect(screen.getByTestId('about-content')).toBeInTheDocument();
    expect(screen.getByTestId('footer')).toBeInTheDocument();
  });
});
