import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import DiagnosisResult from '../components/DiagnosisResult';

describe('DiagnosisResult', () => {
  const selectedFile = new File(['dummy content'], 'example.png', { type: 'image/png' });

  test('renders with provided props', () => {
    const diagnosis = 'Some diagnosis';
    const onGoBack = jest.fn();

    render(
      <DiagnosisResult
        selectedFile={selectedFile}
        diagnosis={diagnosis}
        onGoBack={onGoBack}
      />
    );

    expect(screen.getByText('Diagnosis Result')).toBeInTheDocument();
    expect(screen.getByText('Selected Image:')).toBeInTheDocument();
    expect(screen.getByText('Diagnosis: Some diagnosis')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Go Back' })).toBeInTheDocument();
  });

  test('calls onGoBack function when "Go Back" button is clicked', () => {
    const onGoBack = jest.fn();
    render(
      <DiagnosisResult
        selectedFile={selectedFile}
        diagnosis="Some diagnosis"
        onGoBack={onGoBack}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: 'Go Back' }));

    expect(onGoBack).toHaveBeenCalledTimes(1);
  });
});
