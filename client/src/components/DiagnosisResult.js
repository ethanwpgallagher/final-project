import React from "react";
import { Typography, Button } from "@material-ui/core";

function DiagnosisResult({selectedFile, diagnosis, onRemoveImage, onGoBack}) {
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