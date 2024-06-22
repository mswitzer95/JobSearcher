import {
    Collapse, Card, CardHeader, CardContent, CardActions, Typography, Link,
    IconButton, Divider
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useEffect, useState } from 'react';
import ThumbUpAltOutlinedIcon from '@mui/icons-material/ThumbUpAltOutlined';
import ThumbDownAltOutlinedIcon from '@mui/icons-material/ThumbDownAltOutlined';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';


function JobPostingCard({ jobPosting }) {
    if (jobPosting === null) { return null; }

    const [expanded, setExpanded] = useState(false);
    const [liked, setLiked] = useState(false);
    const [disliked, setDisliked] = useState(false);

    const handleLikeClick = () => {
        let newLiked = !liked;
        setLiked(newLiked);
        if (newLiked) { setDisliked(false); }
    };

    const handleDislikeClick = () => {
        let newDisliked = !disliked;
        setDisliked(newDisliked);
        if (newDisliked) { setLiked(false); }
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
            <CardHeader
                title={title}
                subheader={company}
                sx={{ pb: 0 }}
                action={
                    <IconButton onClick={() => { setExpanded(!expanded); }}>
                        <ExpandMoreIcon
                            sx={{
                                transform: !expanded ? 'rotate(180deg)' : ''
                            }} />
                    </IconButton>
                } />
            <CardHeader subheader={locationsSubheader} sx={{ py: 0 }} />
            <CardHeader subheader={paySubheader} sx={{ py: 0 }} />
            <CardHeader
                subheader={
                    <Link href={link}>Link to posting</Link>
                }
                sx={{ py: 0 }} />
            <CardActions sx={{ pt: 0 }}>
                <IconButton onClick={() => handleLikeClick()}>
                    {liked
                        ? <ThumbUpIcon />
                        : <ThumbUpAltOutlinedIcon />}
                </IconButton>
                <IconButton onClick={() => handleDislikeClick()}>
                    {disliked
                        ? <ThumbDownIcon />
                        : <ThumbDownAltOutlinedIcon />}
                </IconButton>
            </CardActions>
            <Collapse in={expanded} timeout='auto' unmountOnExit>
                <Divider />
                <CardContent>
                    <Typography variant='h6'>Job Description</Typography>
                    <JobDescription jobDescriptionString={description} />
                </CardContent>
            </Collapse>
        </Card>
    );
};


function JobDescription({ jobDescriptionString }) {
    const paragraphs = jobDescriptionString.split('\n');
    const components = paragraphs.map((paragraph, index) =>
        <Typography
            paragraph={paragraph.replace(/\s/g, '').length !== 0} 
            variant='body2' 
            key={index}>
            {paragraph}
        </Typography>
    );
    return components;
};

export { JobPostingCard };