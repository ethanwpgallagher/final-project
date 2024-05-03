import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import DiagnosisContent from '../components/DiagnosisContent';

describe('DiagnosisContent', () => {
  // checks the component loads 
  test('renders without crashing', () => {
    render(<DiagnosisContent handleFileChange={() => {}} />);
    // check the diagnose button renders
    expect(screen.getByText('Diagnose DR')).toBeInTheDocument();
  });

  // checks the upload file button renders
  test('shows upload button when not loading and no file selected', () => {
    render(<DiagnosisContent handleFileChange={() => {}} />);
    expect(screen.getByText('Upload retinal image')).toBeInTheDocument();
  });
});
