import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { MenuItem, Typography, Select, Checkbox, ListItemText, FormControlLabel } from '@material-ui/core';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import { ConfusionMatrix } from 'react-confusion-matrix';

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

  const [logFetch, setLogFetch] = useState(null);

  const [chartLabels, setChartLabels] = useState([]);
  const [chartData, setChartData] = useState({ datasets: [] });
  
  const [confMatLabels, setConfMatLabels] = useState([]);
  const [confMatData, setConfMatData] = useState([]);

  useEffect(() => {
    fetchModelOptionsandLogData();
  }, []);

  useEffect(() => {
    if (selectedModels.length > 0 && (selectedAnalysisOptions.training || selectedAnalysisOptions.test)) {
      changeGraphData();
    }
  }, [selectedModels, selectedAnalysisOptions]);
  

  const fetchModelOptionsandLogData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/get_saved_models');
      if (response.status !== 200) {
        throw new Error('Could not fetch data');
      }
      const data = response.data;
      setModels(data);

      const formData = new FormData();
      formData.append('models', data.join(','));

      const logResponse = await fetch('http://localhost:5000/get_model_analysis', {
        method: 'POST',
        body: formData,
      });

      if (!logResponse.ok) {
        console.error('Error:', logResponse.statusText);
        return;
      }

      const result = await logResponse.json();
      setLogFetch(result);

    } catch (error) {
      console.log(error.message);
    }
  };

  function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  const changeGraphData = async () => {
    try {
        const trainTestBoth = selectedAnalysisOptions.training ? 'training' : selectedAnalysisOptions.test ? 'test' : 'both';
        var labels = [];
        const datasets = [];
        if (trainTestBoth === 'training') {
          selectedModels.forEach(modelName => {
              const modelEpochData = logFetch.epoch_data[modelName.split('.')[0]];
              if (modelEpochData) {
                  const modelLossData = [];
                  const modelAccuracyData = [];
                  const modelValLossData = [];
                  const modelValAccuracyData = [];
                  for (const epochNum in modelEpochData) {
                      const epochData = modelEpochData[epochNum];
                      modelLossData.push(epochData.loss);
                      modelAccuracyData.push(epochData.accuracy);
                      modelValLossData.push(epochData.val_loss);
                      modelValAccuracyData.push(epochData.val_accuracy)
                      labels.push(epochNum.toString());
                  }
                  datasets.push({
                      label: `${modelName} - Loss`,
                      data: modelLossData,
                      borderColor: getRandomColor(),
                      backgroundColor: 'rgba(255, 99, 132, 0.2)',
                  });
                  datasets.push({
                      label: `${modelName} - Accuracy`,
                      data: modelAccuracyData,
                      borderColor: getRandomColor(),
                      backgroundColor: 'rgba(54, 162, 235, 0.2)',
                  });
                  datasets.push({
                      label: `${modelName} - Validation Loss`,
                      data: modelValLossData,
                      borderColor: getRandomColor(),
                      backgroundColor: 'rgba(255, 206, 86, 0.2)',
                  });
                  datasets.push({
                      label: `${modelName} - Validation Accuracy`,
                      data: modelValAccuracyData,
                      borderColor: getRandomColor(),
                      backgroundColor: 'rgba(75, 192, 192, 0.2)',
                  });
              }
          });
          setChartLabels(Array.from(labels));
          setChartData({ datasets });

          console.log('Labels: ', chartLabels);
          console.log('Data: ', chartData);
        
        } else if (trainTestBoth === 'test') {
          selectedModels.forEach(modelName => {
            const modelResultData = logFetch.result_data[modelName.split('.')[0]];
            if (modelResultData) {
              const modelTestAccuracy = modelResultData['Accuracy'];
              const modelF1Score = modelResultData['F1 Score'];
              const modelSensitivity = modelResultData['Sensitivity'];
              const modelSpecificity = modelResultData['Specificity'];
              
              datasets.push({
                label: `${modelName} - Test Accuracy`,
                data: [modelTestAccuracy*100],
                borderColor: getRandomColor(),
                backgroundColor: getRandomColor(),
              });

              datasets.push({
                label: `${modelName} - F1 Score`,
                data: [modelF1Score*100],
                borderColor: getRandomColor(),
                backgroundColor: getRandomColor(),
              });

              datasets.push({
                label: `${modelName} - Sensitivity`,
                data: modelSensitivity.map(value => value * 100),
                borderColor: getRandomColor(),
                backgroundColor: getRandomColor(),
              });

              datasets.push({
                label: `${modelName} - Specificity`,
                data: modelSpecificity.map(value => value * 100),
                borderColor: getRandomColor(),
                backgroundColor: getRandomColor(),
              });
              const confusionMatrixLabels = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR'];
              const modelConfMatrix = modelResultData['Confusion Matrix'];
              setConfMatLabels(confusionMatrixLabels);
              setConfMatData(modelConfMatrix);
            }
          });
        } else {
          console.log('TODO');
        }
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
          <Line data={{ labels: chartLabels, datasets: chartData.datasets }} />
      </div>
      { confMatData && confMatLabels && (
        <div className={classes.confMatContainer}>
              <ConfusionMatrix data={confMatData} labels={confMatLabels}/>
        </div>
      )}
      </div>
    </main>
  );
}

export default AnalysisContent;

