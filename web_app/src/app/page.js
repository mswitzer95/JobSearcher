'use client';

import { JobPostingCard } from './components/JobPostingCard';
import { AppBar } from './components/AppBar';
import React, { useEffect, useState } from 'react';
import { Box } from '@mui/material';


/**
 * The main page of the application
 */
export default function Home() {
    const [jobPostings, setJobPostings] = useState({});

    const fetchJobPostings = async () => {
        let response = await fetch('/scraper_results.json');
        let jobPostingsArray = await response.json();
        setJobPostings(Object.assign({}, jobPostingsArray));
    };

    useEffect(() => {
        fetchJobPostings();
    }, []);

    if (Object.keys(jobPostings).length === 0) { return null; };

    return (
        <>
            <AppBar jobPostings={jobPostings} />
            <Box>
            {
                Object.entries(jobPostings).map(entry =>
                    <React.Fragment key={entry[0]}>
                        <Box sx={{ py: 2 }} >
                            <JobPostingCard jobPosting={entry[1]} />
                        </Box>
                    </React.Fragment>
                )
            }
            </Box>
        </>
    );
}
