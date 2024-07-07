import { useEffect, useState } from 'react';
import {
    Box, AppBar as MUIAppBar, Toolbar, Grid, Typography
} from '@mui/material';
import { SearchBar } from './search/SearchBar';


function AppBar({ jobPostings }) {
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
                        <SearchBar jobPostings={jobPostings} />
                    </Grid>
                </Toolbar>
            </MUIAppBar>
            <Toolbar />
        </Box>
    );
}

export { AppBar };