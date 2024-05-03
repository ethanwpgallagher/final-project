import React from "react";
import PropTypes from 'prop-types';
import { Typography, Button } from "@mui/material";

// defines props for correct usage
DiagnosisResult.propTypes = {
    selectedFile: PropTypes.object,
    diagnosis: PropTypes.string,
    onGoBack: PropTypes.func.isRequired,
};

function DiagnosisResult({ selectedFile, diagnosis, onGoBack }) {
    return (
        <div>
            <Typography variant="h6">Diagnosis Result</Typography>
            {/* display the selected image if it exists */}
            {selectedFile && (
                <div>
                    <Typography variant="subtitle1">Selected Image:</Typography>
                    <img
                        src={URL.createObjectURL(selectedFile)}
                        alt='Selected Retina'
                        style={{ maxWidth: '100%', maxHeight: '400px', margin: '20px 0'}}
                    />
                </div>
            )}
            <Typography variant="body1">Diagnosis: {diagnosis}</Typography>
            <Button variant="contained" onClick={onGoBack} sx={{ bgcolor: 'primary.main', '&:hover': { bgcolor: 'primary.dark' } }}>Go Back</Button>
        </div>
    );
}

export default DiagnosisResult;
