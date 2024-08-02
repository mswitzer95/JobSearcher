import React, { useEffect, useState } from 'react';
import { createSearchableObj, objectMatches, parseString } from './search';
import {
    TextField, IconButton, InputAdornment, Tooltip, Typography
} from '@mui/material';
import CancelIcon from '@mui/icons-material/Cancel';

const tooltipText =
    `Enter your query here. Mulitple terms will be treated as an 'OR' ` +
    `search. Phrases should be surrounded with double quotes, such as ` +
    `"business analyst". You can also search the 'title', 'company', and ` +
    `'description' fields specifically by separating the field and term ` +
    `with a colon, such as 'title:analyst'; if no field is specified for a ` +
    `term, all fields will be searched.`;

const fieldsToSearch = [
    'title', 'description', 'company'
];

/**
 * A React component representing a search bar
 * 
 * @param {object} jobPostings - The job postings as an object/dictionary
 * @param {function} setSearchResultIds - A React state setter for the 
 *      array of keys of which job postings are search results
 * @returns {object} SearchBar - The React component
 */
function SearchBar({ jobPostings, setSearchResultIds }) {
    const [searchableJobPostings, setSearchableJobPostings] = useState({});
    const [searchValue, setSearchValue] = useState('');
    const [label, setLabel] = useState('Search...');

    useEffect(() => {
        let newSearchableJobPostings = Object.fromEntries(
            Object.entries(jobPostings).map(e1 => [
                e1[0], createSearchableObj(
                    Object.fromEntries(
                        Object.entries(e1[1].postingInfo).filter((e2) =>
                            fieldsToSearch.includes(e2[0]))
                    )
                )
            ])
        );
        setSearchableJobPostings(newSearchableJobPostings);
    }, [jobPostings]);

    useEffect(() => {
        let matchingPostingsIds;
        if (searchValue === '') {
            matchingPostingsIds = Object.keys(searchableJobPostings);
        }
        else {
            let searchQueries = parseString(searchValue);
            matchingPostingsIds =
                Object.entries(searchableJobPostings).filter((entry) =>
                    objectMatches(entry[1], searchQueries)
                ).map(entry => entry[0]);
        }
        setSearchResultIds(matchingPostingsIds);
        setLabel(
            'Search... (' +
            `${matchingPostingsIds.length}/` +
            `${Object.keys(searchableJobPostings).length})`);
    }, [searchValue, searchableJobPostings]);

    function handleSearchValueChange(event) {
        setSearchValue(event.target.value);
    }

    const inputProps = searchValue !== '' ? {
        endAdornment: (
            <InputAdornment position='end'>
                <IconButton onClick={() => { setSearchValue(''); }}>
                    <CancelIcon />
                </IconButton>
            </InputAdornment>
        )
    } : {};

    return (
        <Tooltip
            title={
                <React.Fragment>
                    <Typography
                    sx={{ p: 1 }}
                    variant='body2' >
                        {tooltipText}
                    </Typography>
                </React.Fragment>
            }
        >
            <TextField
                fullWidth
                label={label}
                variant='filled'
                value={searchValue}
                onChange={handleSearchValueChange}
                sx={{
                    width: 'auto',
                    backgroundColor: 'white'
                }}
                InputProps={inputProps} />
        </Tooltip>
    )
}


export { SearchBar };