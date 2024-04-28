import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import AnalysisContent from '../components/AnalysisContent';

jest.mock('axios');

describe('AnalysisContent', () => {
  beforeEach(() => {
    axios.get.mockResolvedValue({
      data: ['Model1', 'Model2'], // Mocked models data
      status: 200
    });
    axios.post.mockResolvedValue({
      data: { /* Mocked analysis data */ },
      status: 200
    });
  });

  test('renders without crashing', async () => {
    await render(<AnalysisContent />);
    await waitFor(() => {
      expect(screen.getByText('Analyse models used')).toBeInTheDocument();
    });
  });

  test('initially shows a message to select a model and analysis option', async () => {
    await render(<AnalysisContent />);
    await waitFor(() => {
      expect(screen.getByText('Please select a model and analysis option to display the graph.')).toBeInTheDocument();
    });
  });
});
