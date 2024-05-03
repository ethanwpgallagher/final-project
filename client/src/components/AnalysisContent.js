import React, { useState, useEffect, useMemo } from 'react';
import { styled } from '@mui/material/styles';
import { MenuItem, Typography, Select, Checkbox, ListItemText, FormControlLabel } from '@mui/material';
import axios from 'axios';
import { Line, Bar } from 'react-chartjs-2';
import 'chart.js/auto';

const PREFIX = 'AnalysisContent';

const Root = styled('div')(({ theme }) => ({
  [`&.${PREFIX}-toolbar`]: theme.mixins.toolbar,
  [`& .${PREFIX}-title`]: {
    flexGrow: 1,
    backgroundColour: theme.palette.background.default,
    padding: theme.spacing(3),
  },
  [`& .${PREFIX}-content`]: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
  [`& .${PREFIX}-fullWidth`]: {
    width: '100%',
  },
  [`& .${PREFIX}-selectContainer`]: {
    display: 'inline-block',
    marginRight: theme.spacing(2),
  },
  [`& .${PREFIX}-chartContainer`]: {
    width: '90vw', 
    height: '40vw',
    margin: theme.spacing(2),
  },
}));

function AnalysisContent() {
  // state hooks for managing the models, analysis options, chart data etc
  const [models, setModels] = useState([]);
  const [selectedModels, setSelectedModels] = useState([]);
  const [selectedAnalysisOptions, setSelectedAnalysisOptions] = useState({
    training: false,
    test: false,
  });

  const [logFetch, setLogFetch] = useState(null);
  
  const [chartLabels, setChartLabels] = useState([]);
  const [chartData, setChartData] = useState({ datasets: [] });
  const [barData, setBarData] = useState({
    labels: [],
    datasets: []
  });
  const [colourMap, setColourMap] = useState({});
  const [selectedTrainMetric, setSelectedTrainMetric] = useState('Accuracy');
  const [selectedTestMetric, setSelectedTestMetric] = useState('Accuracy');

  // assigning a colour for each models metric to be used
  const assignColoursToModel = (modelName) => {
    const lossColour = getRandomColour();
    const accuracyColour = getRandomColour();
    const valLossColour = getRandomColour();
    const valAccuracyColour = getRandomColour();
    const testAccuracyColour = getRandomColour();
    const f1ScoreColour = getRandomColour();
    const sensitivityColours = Array.from({ length: 5 }, () => getRandomColour());
    const specificityColours = Array.from({ length: 5 }, () => getRandomColour());

  
    setColourMap(prevColourMap => ({
      ...prevColourMap,
      [modelName]: {
        loss: lossColour,
        accuracy: accuracyColour,
        valLoss: valLossColour,
        valAccuracy: valAccuracyColour,
        "Test Accuracy": testAccuracyColour,
        "F1 Score": f1ScoreColour,
        "Sensitivity": sensitivityColours,
        "Specificity": specificityColours
      }
    }));
  }

  const getColoursForModel = (modelName) => {
    if (colourMap[modelName]) {
      return colourMap[modelName];
    }
  
    assignColoursToModel(modelName);
    return colourMap[modelName];
  }

  const updateBarData = (newLabels, newDatasets) => {
    setBarData({
      labels: newLabels,
      datasets: newDatasets
    })
  }
    
  useEffect(() => {
    fetchModelOptionsandLogData();
  }, []);
  
  // assigns the colours set earlier to the models and changes the graph data
  useEffect(() => {
    selectedModels.forEach(modelName => {
      if (!colourMap[modelName]) {
        assignColoursToModel(modelName);
      }
    });
    if (selectedModels.length > 0 && (selectedAnalysisOptions.training || selectedAnalysisOptions.test)) {
      changeGraphData();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedModels, selectedAnalysisOptions, colourMap, selectedTrainMetric, selectedTestMetric]);  

  // function to fetch model options and log data from the server
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

  function getRandomColour() {
    const letters = '0123456789ABCDEF';
    let colour = '#';
    for (let i = 0; i < 6; i++) {
        colour += letters[Math.floor(Math.random() * 16)];
    }
    return colour;
  }

  // updates the chart and bar data when the training and testing metric selection changes
  useEffect(() => {
    console.log('*USE EFFECT SECTION');
    console.log(chartData);
    console.log(barData);
    console.log(selectedTrainMetric);
    console.log(selectedTestMetric);
    console.log('*END USE EFFECT SECTION');
  }, [chartData, barData, selectedTestMetric, selectedTrainMetric]);

  // changes the graph data based on what the selected models and metrics are
  const changeGraphData = async () => {
    if (!logFetch || !logFetch.epoch_data || !logFetch.result_data || selectedModels.length < 1) return;
    var labels = [];
    let datasets = [];
    try {
      if (selectedAnalysisOptions.training && selectedTrainMetric) {
        datasets = [];
        
        selectedModels.forEach(modelName => {
          const colours = getColoursForModel(modelName);
          const modelEpochData = logFetch.epoch_data[modelName.split('.')[0]];
           // training data
          if (modelEpochData) {
            const modelMetricData = [];
            const modelMetricValData = []
            Object.keys(modelEpochData).forEach(epochNum => {
              const epochData = modelEpochData[epochNum];
              if (selectedTrainMetric === 'Accuracy'){
                let metricValue = epochData[selectedTrainMetric.toLowerCase()] * 100;
                let valMetricValue = epochData['val_accuracy'] * 100;
                modelMetricData.push(metricValue);
                modelMetricValData.push(valMetricValue)
              }
              if (selectedTrainMetric === 'Loss'){
                let metricValue = epochData[selectedTrainMetric.toLowerCase()];
                let valMetricValue = epochData['val_loss'];
                modelMetricData.push(metricValue);
                modelMetricValData.push(valMetricValue)
              }
              labels.push(`Epoch ${epochNum}`);
            });

            datasets.push({
              label: `${modelName} - ${selectedTrainMetric}`,
              data: modelMetricData,
              borderColor: colours[selectedTrainMetric.toLowerCase()],
              backgroundColor: colours[selectedTrainMetric.toLowerCase()],
            });
            if (selectedTrainMetric === 'Accuracy') {
              datasets.push({
                label: `${modelName} - Validation Accuracy`,
                data: modelMetricValData,
                borderColor: colours['valAccuracy'],
                backgroundColor: colours['valAccuracy'],
              });
            }
            if (selectedTrainMetric === 'Loss') {
              datasets.push({
                label: `${modelName} - Validation Loss`,
                data: modelMetricValData,
                borderColor: colours['valLoss'],
                backgroundColor: colours['valLoss'],
              });
            }
          }
        });
        
        const maxEpochs = Math.max(...selectedModels.map(modelName => {
          const modelEpochData = logFetch.epoch_data[modelName.split('.')[0]];
          return modelEpochData ? Object.keys(modelEpochData).length : 0;
        }));
        const commonLabels = Array.from({length: maxEpochs}, (_, i) => (i+1).toString());
        setChartLabels(commonLabels);
        setChartData({ datasets });
      }

      // testing metric selected
      if (selectedAnalysisOptions.test && selectedTestMetric) {
        let barDatasets = [];
        let barLabels = selectedTestMetric === 'Sensitivity' || selectedTestMetric === 'Specificity'
          ? [`Class 0 ${selectedTestMetric}`, `Class 1 ${selectedTestMetric}`, `Class 2 ${selectedTestMetric}`, `Class 3 ${selectedTestMetric}`, `Class 4 ${selectedTestMetric}`]
          : [selectedTestMetric];
        
        selectedModels.forEach(modelName => {
          const modelResultData = JSON.parse(logFetch.result_data[modelName.split('.')[0]]);
          if (modelResultData) {
            const colours = getColoursForModel(modelName);
            const metricValues = modelResultData[selectedTestMetric];
            
            let datasetData = Array.isArray(metricValues) 
              ? metricValues.map(value => value * 100)
              : [metricValues * 100];
            
            const metricDataset = {
              label: modelName,
              backgroundColor: colours[selectedTestMetric],
              data: datasetData,
            };
      
            barDatasets.push(metricDataset);
          }
        });
      
        updateBarData(barLabels, barDatasets);
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
      training: false,
      test: false,
      [event.target.name]: event.target.checked,
    });
  };

  // sets the options for the training data chart
  const chartOptions = useMemo(() => {
    const isAccuracyMetric = ['Accuracy'].includes(selectedTrainMetric);
  
    return {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          min: 0,
          max: isAccuracyMetric ? 100 : undefined, 
          ticks: {
            // Only append '%' for accuracy metrics
            callback: function(value) {
              return isAccuracyMetric ? `${value}%` : value;
            }
          },
          title: {
            display: true,
            text: (() => {
              if (selectedTrainMetric === 'Accuracy') return 'Percentage';
              else if (selectedTrainMetric === 'Loss') return 'Loss';
              return 'Value';
            })(),
          }
        },
        x: {
          ticks: {
            maxTicksLimit: 20
          },
          title: {
            display: true,
            text: 'Epochs'
          }
        },
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
      }
    };
  }, [selectedTrainMetric]);

  // options for the bar graphs for the testing metrics
  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        min: 0,
        max: 100,
        ticks: {
          callback: function(value) {
            return value + '%';
          }
        },
        title: {
          display: true,
          text: 'Percentage'
        }
      },
      x: {
        ticks: {
          maxTicksLimit: 100
        },
      },
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
    }
  };

  // render the component information
  return (
    <Root className={PREFIX}>
      <main className={`${PREFIX}-fullWidth`}>
        <div className={`${PREFIX}-toolbar`} />
        <div className={`${PREFIX}-title`}>
          <Typography variant='h6'>Analyse models used</Typography>
        </div>
        <div className={`${PREFIX}-content`}>
          <div className={`${PREFIX}-selectContainer`}>
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
          <div className={`${PREFIX}-selectContainer`}>
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
          <div className={`${PREFIX}-selectContainer`}>
            {selectedAnalysisOptions.test && (
              <Select
                value={selectedTestMetric}
                onChange={(event) => setSelectedTestMetric(String(event.target.value))}
                displayEmpty
                renderValue={(selected) => selected || 'Select Metric'}
              >
                <MenuItem value="Accuracy">Accuracy</MenuItem>
                <MenuItem value="F1 Score">F1 Score</MenuItem>
                <MenuItem value="Sensitivity">Sensitivity</MenuItem>
                <MenuItem value="Specificity">Specificity</MenuItem>
              </Select>
            )}
            {selectedAnalysisOptions.training && (
              <Select
                value={selectedTrainMetric}
                onChange={(event) => setSelectedTrainMetric(String(event.target.value))}
                displayEmpty
                renderValue={(selected) => selected || 'Select Metric'}
              >
                <MenuItem value="Accuracy">Accuracy</MenuItem>
                <MenuItem value="Loss">Loss</MenuItem>
              </Select>
            )}
          </div>
          {
            selectedModels.length > 0 && selectedAnalysisOptions.training ? (
              <div className={`${PREFIX}-chartContainer`}>
                <Line data={{ labels: chartLabels, datasets: chartData.datasets }} options={chartOptions} />
              </div>
            ) : selectedModels.length > 0 && selectedAnalysisOptions.test ? (
              <div className={`${PREFIX}-chartContainer`}>
                <Bar key={JSON.stringify(barData)} data={barData} options={barOptions}/>
              </div>
            ) : (
              <div className={`${PREFIX}-chartContainer`}>
                <Typography variant="subtitle1">Please select a model and analysis option to display the graph.</Typography>
              </div>
            )
          }
        </div>
      </main>
    </Root>
  );
}

export default AnalysisContent;