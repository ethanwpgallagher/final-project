import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import AnalysisContent from './../components/AnalysisContent'; // Adjust the import path as necessary

// Mocking axios for API calls
jest.mock('axios');

// Mock data for models and analysis
const modelsMock = ['Model1', 'Model2'];
const analysisMock = {
  epoch_data: { Model1: [], Model2: [] },
  result_data: { Model1: [], Model2: [] },
};

beforeEach(() => {
  // Setup mock response for get_saved_models
  axios.get.mockResolvedValueOnce({ status: 200, data: modelsMock });
  // Setup mock response for get_model_analysis
  axios.post.mockResolvedValueOnce({ status: 200, data: analysisMock });
});

describe('AnalysisContent Component', () => {
  test('renders and displays initial UI elements', async () => {
    render(<AnalysisContent />);

    // Ensure the component makes the API call and loads the model options
    await waitFor(() => {
      expect(screen.getByText('Choose model')).toBeInTheDocument();
    });

    modelsMock.forEach(model => {
      expect(screen.getByText(model)).toBeInTheDocument();
    });

    expect(screen.getByText('Analyse models used')).toBeInTheDocument();
    expect(screen.getByText('Please select a model and analysis option to display the graph.')).toBeInTheDocument();
  });

  test('allows user to select models and analysis options', async () => {
    render(<AnalysisContent />);

    // Simulating user selecting a model
    await waitFor(() => fireEvent.mouseDown(screen.getByText('Choose model')));
    fireEvent.click(screen.getByText(modelsMock[0]));

    // Simulating user selecting an analysis option
    fireEvent.click(screen.getByLabelText('Training'));

    // Expect selectedModel and selectedAnalysisOptions state to be updated, which is indirectly checked by the change in the UI
    expect(screen.queryByText('Please select a model and analysis option to display the graph.')).not.toBeInTheDocument();
  });

  // Further tests could simulate submitting the form and checking for the expected API call with the correct parameters,
  // as well as testing the error handling logic by mocking a failed API call.
});

