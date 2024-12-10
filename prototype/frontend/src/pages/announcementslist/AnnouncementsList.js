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

    useEffect(() => {
        setSearchParams({page: currentPage, page_size: pageSize});
        getAnnouncements(currentPage, pageSize).then((response) => {
            setAnnouncements(response);
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
                            authorName={'Пока проблемы с тем, чтобы получить имя автора...'}
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
                    <CustomTextField sx={{width: '100%'}} label="Группа или имя пользователя"/>
                    <CustomTextField sx={{width: '100%'}} label="Дата"/>
                    <CustomTextField sx={{width: '100%'}} label="Тег"/>
                    <CustomButton variant='contained' sx={{alignSelf: 'end'}}>Применить</CustomButton>
                </div>
            </div>
        </div>
    </>;
}
