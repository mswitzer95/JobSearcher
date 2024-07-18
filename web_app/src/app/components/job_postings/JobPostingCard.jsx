import {
    Card, CardHeader, CardActions, Typography, Link, IconButton, Dialog, 
    DialogTitle, DialogContent, Grid
} from '@mui/material';
import { useEffect, useState } from 'react';
import ThumbUpAltOutlinedIcon from '@mui/icons-material/ThumbUpAltOutlined';
import ThumbDownAltOutlinedIcon from
    '@mui/icons-material/ThumbDownAltOutlined';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import CloseIcon from '@mui/icons-material/Close';


/**
 * A React component representing a job posting as a MUI card
 * 
 * @param {object} jobPosting - The job posting as a dictionary/JSON object
 * @returns {object} JobPostingCard - the posting as a React component
 */
function JobPostingCard({ jobPosting }) {
    if (jobPosting === null) { return null; }

    const [open, setOpen] = useState(false);
    const [liked, setLiked] = useState(false);
    const [disliked, setDisliked] = useState(false);

    const handleThumbClick = (
        thumbStatus, thumbStatusSetter, otherThumbStatusSetter) => {
        let newThumbStatus = !thumbStatus;
        thumbStatusSetter(newThumbStatus);
        if (newThumbStatus) { otherThumbStatusSetter(false); }
    };

    const title = jobPosting.title;
    const company = jobPosting.company;
    const description = jobPosting.description;
    const pay = jobPosting.pay;
    const locations = jobPosting.locations;
    const link = jobPosting.link; 

    const locationsSubheader = 'Locations: ' +
        (locations.length > 0 ? locations.join('; ') : 'N/A');

    const paySubheader = `Pay: ${pay !== null ? pay : 'N/A'}`;

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
                        onClick={() => { setOpen(true); }}>
                        Job Description
                    </Link>
                } />
            <CardActions sx={{ pt: 1 }}>
                <Grid
                    container
                    direction='row'
                    justifyContent='space-between'
                    alignItems='center' >
                    <IconButton
                        onClick={() =>
                            handleThumbClick(
                                liked, setLiked, setDisliked)}>
                        {liked
                            ? <ThumbUpIcon fontSize='large' />
                            : <ThumbUpAltOutlinedIcon fontSize='large' />}
                    </IconButton>
                    <IconButton
                        onClick={() =>
                            handleThumbClick(
                                disliked, setDisliked, setLiked)}>
                        {disliked
                            ? <ThumbDownIcon fontSize='large' />
                            : <ThumbDownAltOutlinedIcon fontSize='large' />}
                    </IconButton>
                </Grid>
            </CardActions>
            <JobDescription
                jobDescriptionString={description}
                open={open}
                setOpen={setOpen} />
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

    const paragraphs = jobDescriptionString.split('\n');
    const textComponents = paragraphs.map((paragraph, index) =>
        <Typography
            gutterBottom={paragraph.replace(/\s/g, '').length !== 0} 
            variant='body2' 
            key={index}>
            {paragraph}
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