// src/components/MenuBar.js
import React from 'react';
import { AppBar, Toolbar, Button, TextField } from '@mui/material';

function MenuBar({ onMatchClick, onSearchChange }) {
    return (
        <AppBar position="static">
            <Toolbar>
                <Button color="inherit" onClick={onMatchClick}>
                    Match Claim
                </Button>
                <TextField
                    variant="outlined"
                    placeholder="Search Caption"
                    onChange={(e) => onSearchChange(e.target.value)}
                />
            </Toolbar>
        </AppBar>
    );
}

export default MenuBar;
