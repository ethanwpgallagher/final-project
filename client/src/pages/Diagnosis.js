import React, { useState } from 'react';
import TopMenu from '../components/TopMenu';
import DiagnosisContent from '../components/DiagnosisContent';
import Footer from '../components/Footer';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => (
    {
    root: 
    {
      display: 'flex',
    },
  }));

function Diagnosis() 
{
    const classes = useStyles();
    const [selectedFile, setSelectedFile] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (event) => 
    {
      try {
          const file = event.target.files[0];

          if (file) {
            if (file.type === 'image/jpeg' || file.type === 'image/png') {
              setSelectedFile(file);
              setError(null);
            } else {
              setSelectedFile(null);
              setError('Invalid file type. Please select a JPEG or PNG file.');
            }
          }
      } catch (error) {
        setSelectedFile(null)
      }
    };
  
    return (
      <div className={classes.root}>
        <TopMenu />
        <DiagnosisContent
            handleFileChange={handleFileChange}
            selectedFile={selectedFile}
            error={error} 
        />
        <Footer />
      </div>
    );
  }
  
  export default Diagnosis;