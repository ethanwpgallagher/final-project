import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Diagnosis from '../pages/Diagnosis';

jest.mock('../components/TopMenu', () => () => <div data-testid="top-menu">Top Menu</div>);
jest.mock('../components/DiagnosisContent', () => ({ handleFileChange }) => (
  <div data-testid="diagnosis-content">
    <input type="file" onChange={handleFileChange} data-testid="file-input" />
  </div>
));
jest.mock('../components/Footer', () => () => <div data-testid="footer">Footer</div>);

describe('Diagnosis', () => {
  test('renders all components', () => {
    render(<Diagnosis />);

    expect(screen.getByTestId('top-menu')).toBeInTheDocument();
    expect(screen.getByTestId('diagnosis-content')).toBeInTheDocument();
    expect(screen.getByTestId('footer')).toBeInTheDocument();
  });

  test('handles file change', () => {
    render(<Diagnosis />);
    const fileInput = screen.getByTestId('file-input');
    const file = new File(['dummy content'], 'example.jpg', { type: 'image/jpeg' });

    fireEvent.change(fileInput, { target: { files: [file] } });
  });
});
