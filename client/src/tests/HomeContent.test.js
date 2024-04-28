import React from 'react';
import { render, screen } from '@testing-library/react';
import HomeContent from '../components/HomeContent';

describe('HomeContent', () => {
  test('renders correctly', () => {
    render(<HomeContent />);

    expect(screen.getByText(/Diabetic Retinopathy Diagnosis Tool and Machine Learning Model Analysis/i)).toBeInTheDocument();
    expect(screen.getByText(/Welcome to/i)).toBeInTheDocument();
  });
});
