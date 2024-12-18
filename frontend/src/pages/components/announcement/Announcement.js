import './Announcement.css';

import React, { useState, useEffect, useContext } from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import SelectTag from '../selecttag/SelectTag.js';
import { UserContext } from '../../../contexts/UserContext.js';

import { getAnnouncementStarred, addStarToAnnouncement } from '../../../requests/Requests.js';

import { ReactComponent as StarIcon } from './assets/star.svg';

const CustomSmallButton = styled(Button)(() => ({
    width: '94px',
    height: '20px',

    backgroundColor: 'var(--primary-color)',
    borderRadius: '10px',

    color: 'var(--contrast-text-color)',
    fontSize: '10px',
    fontWeight: 'normal',
    textTransform: 'none'
}));

export default function Announcement(props) {

    const [authentifiedUserId, setAuthentifiedUserId] = useContext(UserContext);
    const [announcementStarred, setAnnouncementStarred] = useState(false);
    const [starsAmount, setStarsAmount] = useState(props.starsAmount);

    useEffect(() => {
        getAnnouncementStarred(authentifiedUserId, props.announcementId).then((response) => {
            setAnnouncementStarred(response);
        });
    }, []);

    const handleStarClick = (event) => {
        if (announcementStarred) {
            addStarToAnnouncement(authentifiedUserId, props.announcementId).then((response) => {
                setAnnouncementStarred(false);
                setStarsAmount(Number(starsAmount) - 1);
            });
        } else {
            addStarToAnnouncement(authentifiedUserId, props.announcementId).then((response) => {
                setAnnouncementStarred(true);
                setStarsAmount(Number(starsAmount) + 1);
            });
        }
    }

    return <>
        <div>
            <div className='visible-layout flex-column width-full' style={{height: 'fit-content', padding: '10px 0 10px 0', gap: '10px'}}>
                <div className='border-box flex-row width-full flex-space' style={{padding: '0 20px 0 20px'}}>
                    <div className='flex-row' style={{gap: '20px'}}>
                        <div className='author-name'>
                            Автор: {props.authorName}
                        </div>
                        <SelectTag 
                            value={props.tag}
                            disabled={true}
                        />
                    </div>
                    <div className='announcement-date'>
                        {props.date}
                    </div>
                </div>
                <div className='border-box flex-row width-full flex-space align-start' style={{padding: '0 20px 0 20px'}}>
                    <div className='annoncement-content width-full'>
                        {props.content}
                    </div>
                    <div className='flex-row align-center flex-center' style={{gap: '5px'}}>
                        <div className='announcement-stars-count'>{starsAmount}</div>
                        <StarIcon
                            style={{
                                stroke: 'var(--primary-color)', 
                                fill: announcementStarred ? 'var(--primary-color)' : 'none'
                            }}
                            onClick={handleStarClick}
                        />
                    </div> 
                </div>
                <div className='flex-row border-box width-full flex-end' style={{padding: '0 20px 0 40px'}}>
                    <CustomSmallButton
                        className='actions-button'
                        variant='contained'
                        onClick={() => {
                            toast("Комментарии запрещены!");
                        }}
                    >
                        Комментарии
                    </CustomSmallButton>
                </div>
            </div>
        </div>
    </>;
}
