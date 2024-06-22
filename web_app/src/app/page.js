'use client';

import { JobPostingCard } from './components/JobPostingCard';
import { useEffect, useState } from 'react';

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

    return jobPostings.map((jobPosting) =>
        <JobPostingCard jobPosting={jobPosting} />
    );
}
