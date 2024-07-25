import { useEffect, useState } from 'react';
import { JobPostingCard } from './JobPostingCard';
import { Box } from '@mui/material';


/**
 * A React component representing a container holding Job Posting cards
 * 
 * @param {Array} jobPostings - An object whose keys are ints and wohse 
 *      values are JSON job postings
 * @param {function} postingAttributeSetter - A function that sets a given 
 *      attribute to a given value for a posting with a given ID. Generally
 *      for setting individual job posting's 'hidden' and 'favorited' 
 *      attributes.
 * @returns JobPostingCardContainer - The React component
 */
function JobPostingCardContainer({jobPostings, postingAttributeSetter }) {
    let cards = Object.entries(jobPostings).map(jobPosting =>
        <Box sx={{ py: 2 }} key={jobPosting[0]} >
            <JobPostingCard
                id={jobPosting[0]}
                jobPosting={jobPosting[1]}
                postingAttributeSetter={postingAttributeSetter} />
        </Box>
    );

    return (
        <Box>
            {cards}
        </Box>
    );
}


export { JobPostingCardContainer };