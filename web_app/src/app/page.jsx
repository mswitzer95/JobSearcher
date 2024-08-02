'use client';

import React, { useEffect, useState } from 'react';
import { JobPostingCardContainer }
    from './components/job_postings/JobPostingCardContainer';
import { AppBar } from './components/app_bar/AppBar';
import { Pagination, createPages } from './components/pagination/Pagination';
import { Box, CssBaseline } from '@mui/material';
import { SnackbarProvider } from 'notistack';


/**
 * The main page of the application
 */
export default function Home({ }) {
    const [jobPostings, setJobPostings] = useState({});
    /* jobPostings should have a structure of:
     * {
     *      {int}: {
     *          favorited: boolean,
     *          hidden: boolean,
     *          postingInfo: {
     *              title: string,
     *              description: string,
     *              company: string,
     *              pay: string,
     *              link: string,
     *              locations: [
     *                  string,
     *              ]
     *          }
     *      }
     * }
     */
    const [searchResultIds, setSearchResultIds] = useState([]);
    const [page, setPage] = useState(1);
    const [idPages, setIdPages] = useState([]);

    /* A function that allows for manipulation of a single attribute of a 
     * single job posting. */
    function setPostingAttribute(id, attributeName, newAttribute) {
        let newPosting = {
            ...jobPostings[id]
        };
        newPosting[attributeName] = newAttribute;
        let newJobPostings = {
            ...jobPostings,
        };
        newJobPostings[id] = newPosting;
        setJobPostings(newJobPostings);
    };

    // Initial fetch of job postings
    useEffect(() => {
        async function fetchJobPostings() {
            let response = await fetch('/scraper_results.json');
            let jobPostingsArray = await response.json();
            setJobPostings(
                Object.assign(
                    {},
                    jobPostingsArray.map(jobPosting => {
                        return {
                            favorited: false,
                            hidden: false,
                            postingInfo: jobPosting
                        };
                    })
                )
            );
        }
        fetchJobPostings();
    }, []);

    // Handling of resetting pagination on search result or posting changes
    useEffect(() => {
        let newIdPages = createPages(
            searchResultIds.filter(searchResultId =>
                jobPostings[searchResultId].hidden === false),
            5
        );
        setIdPages(newIdPages);
        if (page > newIdPages.length) {
            setPage(newIdPages.length);
        }
    }, [searchResultIds, jobPostings]);
    useEffect(() => {
        setPage(1);
    }, [JSON.stringify(searchResultIds)]);

    if (jobPostings.length === 0) { return null; }

    let pagePostings = Object.fromEntries(
        idPages.length > 0
            ? idPages.at(page - 1).map(postingId =>
                [postingId, jobPostings[postingId]])
            : []
    );

    // Scroll to top on pagination
    useEffect(() => {
        window.scrollTo(0, 0);
    }, [page]);

    return (
        <React.Fragment>
            <CssBaseline>
                <SnackbarProvider autoHideDuration={3000}>
                    <Box>
                        <AppBar
                            jobPostings={jobPostings}
                            setSearchResultIds={setSearchResultIds} />
                        <Pagination
                            pageCount={idPages.length}
                            page={page}
                            setPage={setPage}
                            sx={{ pt: 2 }} />
                        <JobPostingCardContainer
                            jobPostings={pagePostings}
                            postingAttributeSetter={setPostingAttribute} />
                        <Pagination
                            pageCount={idPages.length}
                            page={page}
                            setPage={setPage}
                            sx={{ pb: 2 }} />
                    </Box>
                </SnackbarProvider>
            </CssBaseline>
        </React.Fragment>
    );
}
