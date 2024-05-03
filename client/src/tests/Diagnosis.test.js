import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Diagnosis from '../pages/Diagnosis';

// mock components
jest.mock('../components/TopMenu', () => () => <div data-testid="top-menu">Top Menu</div>);
jest.mock('../components/DiagnosisContent', () => ({ handleFileChange }) => (
  <div data-testid="diagnosis-content">
    <input type="file" onChange={handleFileChange} data-testid="file-input" />
  </div>
));
jest.mock('../components/Footer', () => () => <div data-testid="footer">Footer</div>);

describe('Diagnosis', () => {
  // checks rendering 
  test('renders all components', () => {
    render(<Diagnosis />);

    // checks content is rendered as intended
    expect(screen.getByTestId('top-menu')).toBeInTheDocument();
    expect(screen.getByTestId('diagnosis-content')).toBeInTheDocument();
    expect(screen.getByTestId('footer')).toBeInTheDocument();
  });

  // checks that when a file is uploaded, the correct events occur
  test('handles file change', () => {
    render(<Diagnosis />);
    const fileInput = screen.getByTestId('file-input');
    const file = new File(['dummy content'], 'example.jpg', { type: 'image/jpeg' });

    fireEvent.change(fileInput, { target: { files: [file] } });
  });
});
