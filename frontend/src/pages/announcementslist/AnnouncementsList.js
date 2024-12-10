import './AnnouncementsList.css';

import React, { useState, useEffect } from 'react';
import { useSearchParams } from "react-router-dom";
import Pagination from '../components/pagination/Pagination.js';
import { CustomTextField, CustomButton } from '../components/CustomMuiComponents.js';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { getAnnouncements } from '../../requests/Requests.js';
import Announcement from '../components/announcement/Announcement.js';

export default function AnnouncementsList(props) {

    const [searchParams, setSearchParams] = useSearchParams();

    const pageSize = 5;
    const [currentPage, setCurrentPage] = useState(1);
    const [announcements, setAnnouncements] = useState([]);

    const [filterAuthor, setFilterAuthor] = useState('');
    const [filterDate, setFilterDate] = useState('');
    const [filterTag, setFilterTag] = useState('');

    const handleFilter = (event) => {
        const filter = {
            producer: filterAuthor,
            date: filterDate,
            tag: filterTag
        }
        getAnnouncements(currentPage, pageSize, filter).then((response) => {
            setAnnouncements(response);
        });
    }

    useEffect(() => {
        setSearchParams({page: currentPage, page_size: pageSize});
        const filter = {
            producer: filterAuthor,
            date: filterDate,
            tag: filterTag
        }
        getAnnouncements(currentPage, pageSize, filter).then((response) => {
            setAnnouncements(response);
            console.log(response);
        });
    }, [currentPage]);

    const handlePreviousClick = (event) => {
        if (currentPage === 1) {
            toast('Ты уже на первой странице!'); 
            return;
        }
        setCurrentPage(currentPage - 1);
    }

    const handleNextClick = (event) => {
        setCurrentPage(currentPage + 1);
    }

    return <>
        <ToastContainer></ToastContainer>
        <div className='flex-row width-full' style={{gap: '20px'}}>
            <Pagination
                pageNumber={currentPage}
                onPreviousClick={handlePreviousClick}
                onNextClick={handleNextClick}
            >
                {
                    announcements.map((announcement) => {
                        return <Announcement
                            key={announcement.announcement._key}
                            announcementId={announcement.announcement._key}
                            authorName={announcement.sender.first_name == undefined ? announcement.sender.name : announcement.sender.first_name}
                            tag={announcement.announcement.tag}
                            date={announcement.announcement.creation_date}
                            content={announcement.announcement.content}
                            starsAmount={announcement.stars.length}
                        ></Announcement>
                    })
                }
            </Pagination>
            <div className='flex-column fit-width' style={{paddingTop: '80px', gap: '20px'}}>
                <div className='visible-layout flex-column flex-center align-start' style={{padding: '20px', gap: '12px', width: '340px'}}>
                    <div className='caption'>Фильтрация</div>
                    <CustomTextField sx={{width: '100%'}} label="Автор" value={filterAuthor} onChange={(event) => {setFilterAuthor(event.target.value)}}/>
                    <CustomTextField sx={{width: '100%'}} label="Дата" value={filterDate} onChange={(event) => {setFilterDate(event.target.value)}}/>
                    <CustomTextField sx={{width: '100%'}} label="Тег" value={filterTag} onChange={(event) => {setFilterTag(event.target.value)}}/>
                    <CustomButton variant='contained' sx={{alignSelf: 'end'}} onClick={handleFilter}>Применить</CustomButton>
                </div>
            </div>
        </div>
    </>;
}
