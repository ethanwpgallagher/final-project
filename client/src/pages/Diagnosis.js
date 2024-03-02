import React, { useState, useEffect } from 'react';
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

    useEffect(() => {
      const savedImageData = localStorage.getItem('selectedImage');
      if (savedImageData) {
        try {
          const byteCharacters = atob(savedImageData);
          const byteNumbers = new Array(byteCharacters.length);
          for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
          }
          const byteArray = new Uint8Array(byteNumbers);
          const blob = new Blob([byteArray], { type: 'image/jpeg' });
  
          const file = new File([blob], 'uploaded_image', { type: blob.type });
          setSelectedFile(file);
          setError(null);
        } catch (error) {
          console.error('Error loading saved image:', error);
          setSelectedFile(null);
          setError('Error loading saved image. Please select a new file.');
        }
      }
    }, []);

    const handleFileChange = (event) => {
      try {
        const file = event.target.files[0];
    
        if (file) {
          if (file.type === 'image/jpeg' || file.type === 'image/png') {
            const reader = new FileReader();
            reader.onloadend = () => {
              // Convert the selected file to Base64
              const base64Data = reader.result.split(',')[1];
              localStorage.setItem('selectedImage', base64Data);
            };
            reader.readAsDataURL(file);
    
            setSelectedFile(file);
            setError(null);
          } else {
            setSelectedFile(null);
            setError('Invalid file type. Please select a JPEG or PNG file.');
          }
        }
      } catch (error) {
        setSelectedFile(null);
        localStorage.removeItem('selectedImage');
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