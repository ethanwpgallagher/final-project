import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Typography, MenuItem, Select, Button, IconButton } from '@material-ui/core';
import CloseIcon from '@material-ui/icons/Close';

const useStyles = makeStyles((theme) => ({
  toolbar: theme.mixins.toolbar,
  title: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
    display: 'flex',
    alignItems: 'center', // Align items vertically
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    textAlign: 'center',
  },
  fullWidth: {
    width: '100%',
  },
  imageContainer: {
    marginTop: theme.spacing(2),
    textAlign: 'center',
    position: 'relative'
  },
  customFileInputContainer: {
    position: 'relative',
    display: 'flex', // Display children in a row
    flexDirection: 'row', // Align children vertically
    alignItems: 'center', // Center children horizontally
    marginBottom: theme.spacing(2),
  },
  customFileInputLabel: {
    cursor: 'pointer',
    padding: '10px 15px',
    backgroundColor: '#3F51B5',  // Customize background color
    color: 'white',             // Customize text color
    borderRadius: '5px',
    fontSize: '16px',
    transition: 'background-color 0.3s',
    zIndex: 1,
    marginBottom: theme.spacing(1),
  },
  hiddenInput: {
    position: 'absolute',
    top: 0,
    left: 0,
    opacity: 0,
    zIndex: 2,
    cursor: 'pointer',
  },
  errorText: {
    color: 'red',
    marginTop: theme.spacing(1),
  },
  uploadedImage: {
    maxWidth: '100%',
    maxHeight: '400px',
    margin: '20px 0',
  },
  select: {
    minWidth: '150px',
    marginRight: theme.spacing(1),
  },
  getDiagnosisButton: {
    marginTop: theme.spacing(2),
  },
  closeIcon: {
    position: 'absolute',
    top: '5px',
    right: '5px',
    color: 'white',
  },
}));

function DiagnosisContent({ handleFileChange, selectedFile, error }) {
  const classes = useStyles();

  const options = ['Alexnet', 'VGG16', 'VGG19', 'SPPNet', 'GoogLeNet'];
  const [selectedOption, setSelectedOption] = React.useState(() => {
    return localStorage.getItem('selectedOption') || '';
  });

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
    localStorage.setItem('selectedOption', event.target.value);
  };

  const handleGetDiagnosis = () => {
    console.log('Getting diagnosis...')
  }

  const handleRemoveImage = () => {
    handleFileChange(null);
  }

  return (
    <main className={classes.fullWidth}>
      <div className={classes.toolbar}>
        <Typography variant='h6'>Diagnose DR</Typography>
      </div>
      <div className={classes.content}>
          {selectedFile && (
            <div className={classes.imageContainer} style={{ position: 'relative' }}>
              <Typography variant="subtitle1">Selected Image:</Typography>
              <div style={{ position: 'relative' }}>
                <img
                  src={URL.createObjectURL(selectedFile)}
                  alt="Selected"
                  className={classes.uploadedImage}
                />
                <IconButton
                  className={classes.closeIcon}
                  onClick={handleRemoveImage}
                >
                  <CloseIcon />
                </IconButton>
              </div>
            </div>
          )}
        <div className={classes.customFileInputContainer}>
          <Select
            value={selectedOption}
            onChange={handleOptionChange}
            className={classes.select}
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
          <label htmlFor="fileInput" className={classes.customFileInputLabel}>
            Upload retinal image
          </label>
          <input
            type="file"
            id="fileInput"
            onChange={handleFileChange}
            capture="user"
            className={classes.hiddenInput}
          />
        </div>
        {selectedFile && selectedOption && (
          <Button
          variant='contained'
          color='primary'
          className={classes.getDiagnosisButton}
          onClick={handleGetDiagnosis}
          >
            Get DR diagnosis
          </Button>
        )}
        {error && (
          <Typography variant="body2" className={classes.errorText}>
            {error}
          </Typography>
        )}
      </div>
    </main>
  );
}

export default DiagnosisContent;