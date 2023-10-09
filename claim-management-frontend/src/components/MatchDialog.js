// src/components/MatchDialog.js
import React, { useState } from 'react';
import { Dialog, DialogTitle, Button, Input } from '@mui/material';

function MatchDialog({ open, onClose, onUpload }) {
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = () => {
        onUpload(selectedFile);
        onClose();
    };

    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>Upload a Picture</DialogTitle>
            <Input type="file" onChange={handleFileChange} />
            <Button onClick={handleUpload}>Upload</Button>
        </Dialog>
    );
}

export default MatchDialog;
