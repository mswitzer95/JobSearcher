'use client';

import { JobPostingCardContainer }
    from './components/job_postings/JobPostingCardContainer';
import { AppBar } from './components/app_bar/AppBar';
import React, { useEffect, useState } from 'react';
import { Box } from '@mui/material';


/**
 * The main page of the application
 */
export default function Home({ }) {
    const [jobPostings, setJobPostings] = useState({});
    const [displayPostingsIds, setDisplayPostingsIds] = useState([]);

    const fetchJobPostings = async () => {
        let response = await fetch('/scraper_results.json');
        let jobPostingsArray = await response.json();
        setJobPostings(Object.assign({}, jobPostingsArray));
    };

    useEffect(() => {
        fetchJobPostings();
    }, []);

    if (jobPostings.length === 0) { return null; }

    return (
        <Box>
            <AppBar
                jobPostings={jobPostings} 
                setDisplayPostingsIds={setDisplayPostingsIds} />
            <JobPostingCardContainer
                jobPostings={jobPostings}
                displayPostingsIds={displayPostingsIds} />
        </Box>
    );
}
