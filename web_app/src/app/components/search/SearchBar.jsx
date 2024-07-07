import { useEffect, useState } from 'react';
import { sanitizeString, createSearchableObj, objectMatches } from './search';
import { TextField } from '@mui/material';

function SearchBar({ jobPostings }) {
    const [searchableJobPostings, setSearchableJobPostings] = useState({});
    const [searchValue, setSearchValue] = useState('');

    useEffect(() => {
        setSearchableJobPostings(
            Object.fromEntries(
                Object.entries(jobPostings).map(entry => [
                    entry[0],
                    createSearchableObj(entry[1])
                ])
            )
        );
    }, []);

    useEffect(() => {
        let searchQuery = sanitizeString(searchValue);
        let matchingPostings =
            Object.entries(searchableJobPostings).filter((entry) =>
                objectMatches(
                    entry[1],
                    ['company', 'description', 'title'],
                    searchQuery));
        console.log(matchingPostings);
    }, [searchValue]);

    function handleSearchValueChange(event) {
        setSearchValue(event.target.value);
    }

    return (
        <TextField
            label='Search...'
            variant='filled'
            value={searchValue}
            onChange={handleSearchValueChange} />
    )
}

export { SearchBar };