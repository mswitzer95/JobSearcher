import { Pagination as MUIPagination, Box, Grid } from '@mui/material';
import { useEffect, useState } from 'react';

/**
 * A React component represneting a pagination element
 * 
 * @param {int} total - The total number of elements to paginate
 * @param {int} step - The number of elements to paginate by at a time
 * @param {int} startIndex - The index of the element whose page is shown in 
 *      the array of elements to paginate
 * @param {function} startIndexSetter - A React state setter for startIndex
 * @returns {object} Pagination - the React component
 */
function Pagination({ total, step, startIndex, startIndexSetter }) {
    const count = Math.ceil(total / step);
    const [startPage, setStartPage] =
        useState(Math.floor(startIndex / step) + 1);
    const [page, setPage] = useState(startPage);
    const handleChange = (event, newPage) => {
        setPage(newPage);
        let newStartIndex = (newPage - 1) * step;
        startIndexSetter(newStartIndex);
    }

    useEffect(() => {
        startIndexSetter(0);
    }, [total, step])
    
    return (
        <Box>
            <Grid
                container
                direction='row'
                alignItems='center'
                justifyContent='center' >
                <MUIPagination
                    count={count}
                    page={page}
                    onChange={handleChange} />
            </Grid>
        </Box>
    );
}


export { Pagination };