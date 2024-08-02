import {
    Card, CardHeader, CardActions, Typography, Link, IconButton, Dialog, 
    DialogTitle, DialogContent, Grid, Button
} from '@mui/material';
import { useEffect, useState } from 'react';
import { useSnackbar } from 'notistack';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import DeleteIcon from '@mui/icons-material/Delete';
import CloseIcon from '@mui/icons-material/Close';


/**
 * A React component representing a job posting as a MUI card
 * 
 * @param {any} id - The posting's ID
 * @param {object} jobPosting - The job posting as a dictionary/JSON object
 * @param {function} postingAttributeSetter - A function that sets a given 
 *      attribute to a given value for a posting with a given ID. Generally
 *      for setting the job posting's 'hidden' and 'favorited' attributes.
 * 
 * @returns {object} JobPostingCard - the posting as a React component
 */
function JobPostingCard({ id, jobPosting, postingAttributeSetter }) {
    if (jobPosting === null) { return null; }

    const [descriptionOpen, setDescriptionOpen] = useState(false);

    const { enqueueSnackbar, closeSnackbar } = useSnackbar();

    const title = jobPosting.postingInfo.title;
    const company = jobPosting.postingInfo.company;
    const description = jobPosting.postingInfo.description;
    const pay = jobPosting.postingInfo.pay;
    const locations = jobPosting.postingInfo.locations;
    const link = jobPosting.postingInfo.link; 

    const locationsSubheader = 'Locations: ' +
        (locations.length > 0 ? locations.join('; ') : 'N/A');

    const paySubheader = 'Pay: ' + (pay !== null ? pay : 'N/A');

    const abbreviatedTitle =
        title.slice(0, 20) + (title.length > 20 ? '...' : '');
    const abbreviatedCompany =
        company.slice(0, 20) + (company.length > 20 ? '...' : '');

    function handleFavoriteClick() {
        let newFavorited = !jobPosting.favorited;
        postingAttributeSetter(id, 'favorited', newFavorited);
        let snackbarText =
            (newFavorited ? 'Favorited ' : 'Unfavorited ') +
            `${abbreviatedTitle} at ${abbreviatedCompany}.`;
        let action = snackbarId => (
            <Button
                onClick={() => {
                    postingAttributeSetter(id, 'favorited', !newFavorited);
                    closeSnackbar(snackbarId);
                }} >
                Undo
            </Button>
        );
        enqueueSnackbar(snackbarText, { action, });
    };

    function handleHideClick() {
        let newHidden = !jobPosting.hidden;
        postingAttributeSetter(id, 'hidden', newHidden);
        let snackbarText =
            (newHidden ? 'Hid ' : 'Unhid ') +
            `${abbreviatedTitle} at ${abbreviatedCompany}.`;
        let action = snackbarId => (
            <Button
                onClick={() => {
                    postingAttributeSetter(id, 'hidden', !newHidden);
                    closeSnackbar(snackbarId);
                }} >
                Undo
            </Button>
        )
        enqueueSnackbar(snackbarText, { action, });
    };

    return (
        <Card variant='outlined'>
            <CardHeader title={title} sx={{ pb: 1 }} />
            <Subheader subheader={company} />
            <Subheader subheader={locationsSubheader} />
            <Subheader subheader={paySubheader} />
            <Subheader
                subheader={
                    <Link
                        href={link}
                        target='_blank'
                        rel='noreferrer'>
                        Link to Posting
                    </Link>
                } />
            <Subheader
                subheader={
                    <Link
                        component='button'
                        onClick={() => { setDescriptionOpen(true); }}>
                        Job Description
                    </Link>
                } />
            <CardActions sx={{ pt: 1 }}>
                <Grid
                    container
                    direction='row'
                    justifyContent='space-between'
                    alignItems='center' >
                    <IconButton onClick={handleFavoriteClick}>
                        {
                            jobPosting.favorited
                                ? <FavoriteIcon fontSize='large' />
                                : <FavoriteBorderIcon fontSize='large' />
                        }
                    </IconButton>
                    <IconButton onClick={handleHideClick}>
                        {
                            jobPosting.hidden
                                ? <DeleteIcon fontSize='large' />
                                : <DeleteOutlineIcon fontSize='large' />
                        }
                    </IconButton>
                </Grid>
            </CardActions>
            <JobDescription
                jobDescriptionString={description}
                open={descriptionOpen}
                setOpen={setDescriptionOpen} />
        </Card>
    );
};


/**
 * A React component representing the job description as a modal
 * 
 * @param {string} jobDescriptionString - The job description text
 * @param {boolean} open - Whether the modal is open
 * @param {functon} setOpen - React state setter for the 'open' variable
 * @returns {object} JobDescription - The React component
 */
function JobDescription({ jobDescriptionString, open, setOpen }) {
    const handleClose = () => { setOpen(false); }

    const textComponents = (
        <Typography
            gutterBottom
            variant='body2'
            style={{ whiteSpace: 'pre-line' }}
        >
            {jobDescriptionString.replace(/[\n]{3,}/g, '\n\n')}
        </Typography>
    );

    const dialog = (
        <Dialog
            open={open}
            onClose={handleClose}
            fullWidth={true}
            maxWidth='md' >
            <DialogTitle>Job Description</DialogTitle>
            <IconButton
                onClick={handleClose}
                sx={{
                    position: 'absolute',
                    right: 8,
                    top: 8
                }}
            >
                <CloseIcon />
            </IconButton>
            <DialogContent dividers>
                {textComponents}
            </DialogContent>
        </Dialog>
    );

    return dialog;
};


/**
 * A React component representing subheader info of the JobPosting card
 * 
 * @param {any} subheader - The content to embed in the card header's subheader
 * @returns {objcet} Subheader - The React component
 */
function Subheader({ subheader }) {
    return (
        <CardHeader subheader={subheader} sx={{ py: 1 }} />
    );
}


export { JobPostingCard };