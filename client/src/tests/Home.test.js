import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../pages/Home';

// creates mock compoments
jest.mock('../components/TopMenu', () => () => <div data-testid="top-menu">Top Menu</div>);
jest.mock('../components/HomeContent', () => () => <div data-testid="home-content">Home Content</div>);
jest.mock('../components/Footer', () => () => <div data-testid="footer">Footer</div>);

describe('Home', () => {
  // check that it renders all components
  test('renders all components', () => {
    render(<Home />);

    // check the content is displayed correctly for mocked components
    expect(screen.getByTestId('top-menu')).toBeInTheDocument();
    expect(screen.getByTestId('home-content')).toBeInTheDocument();
    expect(screen.getByTestId('footer')).toBeInTheDocument();
  });
});
