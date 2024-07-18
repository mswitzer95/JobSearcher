import { useEffect, useState } from 'react';
import { JobPostingCard } from './JobPostingCard';
import { Pagination } from './Pagination';
import { Box } from '@mui/material';


/**
 * A React component representing a container holding Job Posting cards
 * 
 * @param {object} jobPostings - An object whose keys are ints and wohse 
 *      values are JSON job postings
 * @param {Array.int} displayPostingsIds - An array of job posting IDs to 
 *      display based on search results
 * @returns JobPostingCardContainer - The React component
 */
function JobPostingCardContainer({ jobPostings, displayPostingsIds }) {
    const [
        displayPostingsStartIndex, setDisplayPostingsStartIndex
    ] = useState(0);
    const [cards, setCards] = useState(null);
    const step = 5;

    useEffect(() => {
        setDisplayPostingsStartIndex(0);
    }, [displayPostingsIds]);

    useEffect(() => {
        let displayPostings =
            Object.entries(jobPostings).filter((entry) =>
                displayPostingsIds.includes(entry[0])
            ).slice(displayPostingsStartIndex, displayPostingsStartIndex + step);
        let newCards = displayPostings.map(displayPosting =>
            <Box sx={{ py: 2 }} key={displayPosting[0]} >
                <JobPostingCard
                    jobPosting={displayPosting[1]} />
            </Box>
        );
        setCards(newCards);
    }, [jobPostings, displayPostingsIds, displayPostingsStartIndex]);

    return (
        <Box>
            {cards}
            <Pagination
                total={displayPostingsIds.length}
                step={step}
                startIndex={displayPostingsStartIndex}
                startIndexSetter={setDisplayPostingsStartIndex} />
        </Box>
    );
}


export { JobPostingCardContainer };