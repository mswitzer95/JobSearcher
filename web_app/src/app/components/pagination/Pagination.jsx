import { useEffect, useState } from 'react';
import { Pagination as MUIPagination, Box, Grid } from '@mui/material';


/**
 * A React component representing a pagination element
 * 
 * @param {int} pageCount - The total number of pages
 * @param {int} page - The current page 
 * @param {function} setPage - A React state setter for the current page
 * @param {object} sx - The styling to apply to the outer box of the component
 * @returns {object} Pagination - the React component
 */
function Pagination({ pageCount, page, setPage, sx }) {
    function handleChange(event, newPage) {
        setPage(newPage);
    }
    
    return (
        <Box sx={sx}>
            <Grid
                container
                direction='row'
                alignItems='center'
                justifyContent='center' >
                <MUIPagination
                    count={pageCount}
                    page={page}
                    onChange={handleChange} />
            </Grid>
        </Box>
    );
}


/**
 * Turns an array into a 2d array of "pages" of the original array
 * 
 * @param {Array} array - The array to manipulate into pages
 * @param {int} elementsPerPage - The desired number of elements per page
 * @returns {Array.Array} pages - The 2d array of pages
 */
function createPages(array, elementsPerPage) {
    let pageCount = Math.ceil(array.length / elementsPerPage);
    let pageStartIndices =
        Array(pageCount).fill().map((i, j) => j * elementsPerPage);
    let pages =
        pageStartIndices.map(index =>
            array.slice(index, index + elementsPerPage));
    return pages;
}


export { Pagination, createPages };