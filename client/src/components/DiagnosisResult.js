import React from "react";
import PropTypes from 'prop-types';
import { Typography, Button } from "@material-ui/core";

DiagnosisResult.propTypes = {
    selectedFile: PropTypes.object,
    diagnosis: PropTypes.string,
    onRemoveImage: PropTypes.func, // Assuming you might use this prop in future
    onGoBack: PropTypes.func.isRequired,
};

function DiagnosisResult({selectedFile, diagnosis, onGoBack}) {
    return (
        <div>
            <Typography variant="h6">Diagnosis Result</Typography>
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
            <Button variant="contained" color="primary" onClick={onGoBack}>Go Back</Button>
        </div>
    );
}

export default DiagnosisResult;