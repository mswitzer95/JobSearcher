import { useEffect, useState } from 'react';
import { ExportButton } from './export/ExportButton';
import { SearchBar } from './search/SearchBar';
import {
    Box, AppBar as MUIAppBar, Toolbar, Grid, Typography
} from '@mui/material';

/**
 * A React component representing an app bar 
 * 
 * @param {object} jobPostings - The job postings as an object/dictionary
 * @param {function} setSearchResultIds - A React state setter for the array 
 *      of keys of which job postings are search results
 * @returns {object} AppBar - The React component
 */
function AppBar({ jobPostings, setSearchResultIds }) {
    let favoritedPostings =
        Object.values(jobPostings).filter(posting => posting.favorited);

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
                        <ExportButton
                            postingsToExport={favoritedPostings}
                            buttonText={'Export Favorites'} />
                        <SearchBar
                            jobPostings={jobPostings}
                            setSearchResultIds={setSearchResultIds} />
                    </Grid>
                </Toolbar>
            </MUIAppBar>
            <Toolbar />
        </Box>
    );
}


export { AppBar };