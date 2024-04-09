import { React, useState, useEffect } from 'react';
import { styled } from '@mui/material/styles';
import { Typography, MenuItem, Select, Button, IconButton, CircularProgress } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import DiagnosisResult from './DiagnosisResult';
import axios from 'axios';
import { PropTypes } from 'prop-types';

const PREFIX = 'DiagnosisContent';

const Root = styled('main')(({ theme }) => ({
  [`&.${PREFIX}-fullWidth`]: {
    width: '100%',
  },
  [`& .${PREFIX}-toolbar`]: theme.mixins.toolbar,
  [`& .${PREFIX}-title`]: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
    display: 'flex',
    alignItems: 'center',
  },
  [`& .${PREFIX}-content`]: {
    flexGrow: 1,
    padding: theme.spacing(3),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    textAlign: 'center',
  },
  [`& .${PREFIX}-imageContainer`]: {
    marginTop: theme.spacing(2),
    textAlign: 'center',
    position: 'relative',
  },
  [`& .${PREFIX}-customFileInputContainer`]: {
    position: 'relative',
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: theme.spacing(2),
  },
  [`& .${PREFIX}-customFileInputLabel`]: {
    cursor: 'pointer',
    padding: '10px 15px',
    backgroundColor: '#3F51B5',
    color: 'white',
    borderRadius: '5px',
    fontSize: '16px',
    transition: 'background-color 0.3s',
    zIndex: 1,
    marginBottom: theme.spacing(1),
  },
  [`& .${PREFIX}-hiddenInput`]: {
    position: 'absolute',
    top: 0,
    left: 0,
    opacity: 0,
    zIndex: 2,
    cursor: 'pointer',
  },
  [`& .${PREFIX}-errorText`]: {
    color: 'red',
    marginTop: theme.spacing(1),
  },
  [`& .${PREFIX}-uploadedImage`]: {
    maxWidth: '100%',
    maxHeight: '400px',
    margin: '20px 0',
  },
  [`& .${PREFIX}-select`]: {
    minWidth: '150px',
    marginRight: theme.spacing(1),
  },
  [`& .${PREFIX}-getDiagnosisButton`]: {
    marginTop: theme.spacing(2),
  },
  [`& .${PREFIX}-closeIcon`]: {
    position: 'absolute',
    top: '5px',
    right: '5px',
    color: 'white',
  },
}));

const drClassToSeverity = {
  '0': 'No DR',
  '1' : 'Mild DR',
  '2': 'Moderate DR',
  '3': 'Severe DR',
  '4': 'Proliferative DR'
}

function DiagnosisContent({ handleFileChange, selectedFile, error }) {
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(() => localStorage.getItem('selectedOption') || '');
  const [loading, setLoading] = useState(false);
  const [diagnosisResult, setDiagnosisResult] = useState(false);

  useEffect(() => {
    fetchModelOptions();
  }, []);

  const fetchModelOptions = async () => {
    try {
      const response = await axios.get('http://localhost:5000/get_saved_models');
      if (response.status != 200) {
        throw new Error('Couldnt fetch data mush');
      }
      const data = response.data;
      setOptions(data)
    } catch (error) {
      console.log(error.message);
    }
  };

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
    localStorage.setItem('selectedOption', event.target.value);
  };

  const handleGetDiagnosis = async () => {
    setLoading(true);
  
    try {
      const formData = new FormData();
      formData.append('selectedOption', selectedOption);
      formData.append('selectedFile', selectedFile);
  
      const response = await fetch('http://localhost:5000/receive_predictions', {
        method: 'POST',
        body: formData,
      });
  
      if (!response.ok) {
        console.error('Error:', response.statusText);
        return;
      }
  
      const result = await response.json();
      setDiagnosisResult(drClassToSeverity[result.diagnosis]);
      console.log(diagnosisResult);
    } catch (error) {
      console.error(error.message);
    } finally {
      setLoading(false);
    }
  };
    
  const handleRemoveImage = () => {
    handleFileChange(null);
    setDiagnosisResult(null);
  };

  const onGoBack = () => {
    setDiagnosisResult(null);
  }

  return (
    <Root className={`${PREFIX}-fullWidth`}>

      <main className={`${PREFIX}-fullWidth`}>
        <div className={`${PREFIX}-toolbar`}>
          <Typography variant='h6'>Diagnose DR</Typography>
        </div>
        <div className={`${PREFIX}-content`}>
          {loading && (
            <div>
              <Typography variant="h6">Loading...</Typography>
              <CircularProgress />
            </div>
          )}
          {!loading && selectedFile && !diagnosisResult && (
            <div className={`${PREFIX}-imageContainer`} style={{ position: 'relative' }}>
              <Typography variant="subtitle1">Selected Image:</Typography>
              <div style={{ position: 'relative' }}>
                <img
                  src={URL.createObjectURL(selectedFile)}
                  alt="Selected"
                  className={`${PREFIX}-uploadedImage`}
                />
                <IconButton
                  className={`${PREFIX}-closeIcon`}
                  onClick={handleRemoveImage}
                >
                  <CloseIcon />
                </IconButton>
              </div>
            </div>
          )}
          {!loading && !diagnosisResult && (
            <div className={`${PREFIX}-customFileInputContainer`}>
              <Select
                value={selectedOption}
                onChange={handleOptionChange}
                className={`${PREFIX}-select`}
                displayEmpty
              >
                <MenuItem value="" disabled>
                  Choose model
                </MenuItem>
                {options.map((option, index) => (
                  <MenuItem key={index} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </Select>
              <label htmlFor="fileInput" className={`${PREFIX}-customFileInputLabel`}>
                Upload retinal image
              </label>
              <input
                type="file"
                id="fileInput"
                onChange={handleFileChange}
                capture="user"
                className={`${PREFIX}-hiddenInput`}
              />
            </div>
          )}
          {!loading && selectedFile && selectedOption && !diagnosisResult && (
            <Button
              variant='contained'
              color='primary'
              className={`${PREFIX}-getDiagnosisButton`}
              onClick={handleGetDiagnosis}
            >
              Get DR diagnosis
            </Button>
          )}
          {diagnosisResult && (
            <DiagnosisResult
            selectedFile={selectedFile}
            diagnosis={diagnosisResult}
            onGoBack={onGoBack}
            />
          )}
          {!loading && error && (
            <Typography variant="body2" className={`${PREFIX}-errorText`}>
              {error}
            </Typography>
          )}
        </div>
      </main>
    </Root>
  );
}

DiagnosisContent.propTypes = {
  handleFileChange: PropTypes.func.isRequired,
  selectedFile: PropTypes.string,
  error: PropTypes.shape({
    message: PropTypes.string,
  }),
};

export default DiagnosisContent;
