import { useEffect, useState } from 'react';
import { Box, Button } from '@mui/material';


/**
 * A React component representing a button that exports postings to CSV
 * @param {Array.object} itemsToExport - The postings to export to CSV
 * @param {string} buttonText - The text to display in the button
 * @returns {object} ExportButton - The React component
 */
function ExportButton({ postingsToExport, buttonText }) {

    function handleClick() {
        let headers, rows;
        if (postingsToExport.length > 0) {
            headers = Object.keys(postingsToExport[0].postingInfo).map(key =>
                typeof key === 'string' ? `\"${key}\"` : key);
            rows = postingsToExport.map(posting =>
                Object.values(posting.postingInfo).map(value => {
                    if (Array.isArray(value)) {
                        value = value.join('; ');
                    }
                    value =
                        typeof value === 'string' ? `\"${value}\"` : value;
                    return value;
                })
            );
            rows.unshift(headers);
        } else {
            rows = [];
        }
        let csvContent =
            encodeURI('data:text/csv;charset=utf-8,')
            + encodeURIComponent(
                rows.map(row => row.join(',')).join('\n'));
        //let encodedUri = encodeURIComponent(csvContent);
        //window.open(encodedUri);
        window.open(csvContent);
    }

    return (
        <Box>
            <Button variant='contained' onClick={handleClick}>
                {buttonText}
            </Button>
        </Box>
    );
}


export { ExportButton };