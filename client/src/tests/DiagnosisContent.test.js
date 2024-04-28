import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import DiagnosisContent from '../components/DiagnosisContent';

describe('DiagnosisContent', () => {
  test('renders without crashing', () => {
    render(<DiagnosisContent handleFileChange={() => {}} />);
    expect(screen.getByText('Diagnose DR')).toBeInTheDocument();
  });

  test('shows upload button when not loading and no file selected', () => {
    render(<DiagnosisContent handleFileChange={() => {}} />);
    expect(screen.getByText('Upload retinal image')).toBeInTheDocument();
  });
});
