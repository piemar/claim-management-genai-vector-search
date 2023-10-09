// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import MenuBar from './components/MenuBar';
import ClaimsList from './components/ClaimsList';
import MatchDialog from './components/MatchDialog';

function App() {
    const FLASK_ENDPOINT_BASEURL = "http://localhost:5000"
    const [claims, setClaims] = useState([]); // Replace with actual data fetching logic
    const [isMatchDialogOpen, setMatchDialogOpen] = useState(false);
    
    const handleMatchClick = () => {
        setMatchDialogOpen(true);
    };
  

    const handleUploadAndMatch = (file) => {
      const formData = new FormData();
      formData.append('file', file);
      axios.post('http://localhost:5000/match', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      }).then((response) => { 
        if(response.data) {
            setClaims(response.data)
          
        }        
      }).catch((error) => {
        console.error('Error fetching data: ', error);
      });   

  }

  
    return (
        <div>
            <MenuBar onMatchClick={handleMatchClick} />
            <ClaimsList claims={claims} />
            <MatchDialog
                open={isMatchDialogOpen}
                onClose={() => setMatchDialogOpen(false)}
                onUpload={handleUploadAndMatch}
            />
        </div>
    );
}

export default App;
