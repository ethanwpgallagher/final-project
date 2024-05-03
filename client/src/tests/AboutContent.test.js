import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import AboutContent from '../components/AboutContent'; // Adjust the import path as necessary

describe('AboutContent', () => {
  // checks the component renders
  test('renders without crashing', () => {
    render(<AboutContent />);
    expect(screen.getByRole('heading', { name: /about this tool/i })).toBeInTheDocument();
  });

  // checks the content is displayed correct
  test('displays the correct description text', () => {
    render(<AboutContent />);
    expect(screen.getByText(/developed by Ethan Gallagher for ECM1234 Individual Project and Literature Review/i)).toBeInTheDocument();
  });
});
