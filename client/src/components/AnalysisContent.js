import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { MenuItem, Typography, Select, Checkbox, ListItemText, FormControlLabel } from '@material-ui/core';
import axios from 'axios';
import { Line } from 'react-chartjs-2'; // Import Line chart from react-chartjs-2
import 'chart.js/auto';

const useStyles = makeStyles(theme => ({
  toolbar: theme.mixins.toolbar,
  title: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
  fullWidth: {
    width: '100%',
  },
  selectContainer: {
    display: 'inline-block', // Align horizontally
    marginRight: theme.spacing(2),
  },
  chartContainer: {
    marginTop: theme.spacing(3),
  },
}));

function AnalysisContent() {
  const classes = useStyles();
  const [models, setModels] = useState([]);
  const [selectedModels, setSelectedModels] = useState([]);
  const [selectedAnalysisOptions, setSelectedAnalysisOptions] = useState({
    training: false,
    test: false,
  });

  useEffect(() => {
    fetchModelOptions();
  }, []);

  const fetchModelOptions = async () => {
    try {
      const response = await axios.get('http://localhost:5000/get_saved_models');
      if (response.status !== 200) {
        throw new Error('Could not fetch data');
      }
      const data = response.data;
      setModels(data);
    } catch (error) {
      console.log(error.message);
    }
  };

  const handleModelChange = (event) => {
    setSelectedModels(event.target.value);
  };

  const handleAnalysisOptionChange = (event) => {
    setSelectedAnalysisOptions({
      ...selectedAnalysisOptions,
      [event.target.name]: event.target.checked,
    });
  };

  // Sample chart data
  const chartData = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
      {
        label: 'Sales',
        data: [65, 59, 80, 81, 56, 55, 40],
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
      {
        label: 'Expenses',
        data: [28, 48, 40, 19, 86, 27, 90],
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  };

  return (
    <main className={classes.fullWidth}>
      <div className={classes.toolbar} />
      <div className={classes.title}>
        <Typography variant='h6'>Analyse models used</Typography>
      </div>
      <div className={classes.content}>
        <div className={classes.selectContainer}>
          <Select
            multiple
            value={selectedModels}
            onChange={handleModelChange}
            displayEmpty
            renderValue={(selected) => selected.join(', ')}
          >
            <MenuItem value="" disabled>
              Choose model
            </MenuItem>
            {models.map((model) => (
              <MenuItem key={model} value={model}>
                <Checkbox checked={selectedModels.indexOf(model) > -1} />
                <ListItemText primary={model} />
              </MenuItem>
            ))}
          </Select>
        </div>
        <div className={classes.selectContainer}>
          <FormControlLabel
            control={
              <Checkbox
                checked={selectedAnalysisOptions.training}
                onChange={handleAnalysisOptionChange}
                name="training"
              />
            }
            label="Training"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={selectedAnalysisOptions.test}
                onChange={handleAnalysisOptionChange}
                name="test"
              />
            }
            label="Test"
          />
        </div>
        <div className={classes.chartContainer}>
          <Line data={chartData} />
        </div>
      </div>
    </main>
  );
}

export default AnalysisContent;
