import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import TopMenu from '../components/TopMenu';

describe('TopMenu Component', () => {
  const renderWithRouter = (component) => {
    return render(<BrowserRouter>{component}</BrowserRouter>);
  };

  // check the component renders and all the links are correct for navigation
  test('renders menu items with correct navigation links', () => {
    renderWithRouter(<TopMenu />);

    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Home').closest('a')).toHaveAttribute('href', '/');

    expect(screen.getByText('Diagnosis Tool')).toBeInTheDocument();
    expect(screen.getByText('Diagnosis Tool').closest('a')).toHaveAttribute('href', '/diagnosis');

    expect(screen.getByText('Model Analysis')).toBeInTheDocument();
    expect(screen.getByText('Model Analysis').closest('a')).toHaveAttribute('href', '/analysis');

    expect(screen.getByText('About')).toBeInTheDocument();
    expect(screen.getByText('About').closest('a')).toHaveAttribute('href', '/about');
  });
});
