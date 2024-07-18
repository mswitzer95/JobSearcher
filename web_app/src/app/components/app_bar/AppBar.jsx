import { useEffect, useState } from 'react';
import {
    Box, AppBar as MUIAppBar, Toolbar, Grid, Typography
} from '@mui/material';
import { SearchBar } from './search/SearchBar';

/**
 * A React component representing an app bar 
 * 
 * @param {object} jobPostings - The job postings as an object/dictionary
 * @param {function} - A React state setter for for the array of keys of which 
 *      job postings to display
 * @returns {object} AppBar - The React component
 */
function AppBar({ jobPostings, setDisplayPostingsIds }) {
    return (
        <Box sx={{ flexGrow: 1 }}>
            <MUIAppBar component='nav'>
                <Toolbar>
                    <Grid
                        container
                        direction='row'
                        justifyContent='space-between'
                        alignItems='center' >
                        <Typography variant='h6'>JobSearcher</Typography>
                        <SearchBar
                            jobPostings={jobPostings}
                            setDisplayPostingsIds={setDisplayPostingsIds} />
                    </Grid>
                </Toolbar>
            </MUIAppBar>
            <Toolbar />
        </Box>
    );
}


export { AppBar };