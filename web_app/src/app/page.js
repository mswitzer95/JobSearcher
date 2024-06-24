'use client';

import { JobPostingCard } from './components/JobPostingCard';
import React, { useEffect, useState } from 'react';
import { Box } from '@mui/material';

export default function Home() {
    const [jobPostings, setJobPostings] = useState([]);

    const fetchJobPostings = async () => {
        let response = await fetch('/scraper_results.json');
        let jobPostings = await response.json();
        setJobPostings(jobPostings);
    };

    useEffect(() => {
        fetchJobPostings();
    }, []);

    if (jobPostings.length === 0) { return null; };

    return jobPostings.map((jobPosting, index) =>
        <React.Fragment key={index}>
            <Box sx={{ py: 2 }} >
                <JobPostingCard jobPosting={jobPosting} />
            </Box>
        </React.Fragment>
    );
}
