import './UsersList.css';

import React, { useState, useEffect } from 'react';
import { useSearchParams } from "react-router-dom";
import Pagination from '../components/pagination/Pagination.js';
import { CustomTextField, CustomButton } from '../components/CustomMuiComponents.js';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { getUsers } from '../../requests/Requests.js';

import { ReactComponent as BigStarIcon } from './assets/big-star.svg';

export default function UsersList(props) {

    const [searchParams, setSearchParams] = useSearchParams();

    const pageSize = 3;
    const [currentPage, setCurrentPage] = useState(1);
    const [users, setUsers] = useState([]);

    const [filterName, setFilterName] = useState('');
    const [filterSurname, setFilterSurname] = useState('');
    const [filterTalent, setFilterTalent] = useState('');
    const [filterGroup, setFilterGroup] = useState('');

    const handleFilter = (event) => {
        const filter = {
            first_name: filterName,
            last_name: filterSurname,
            talents: filterTalent,
            groups: filterGroup
        }
        getUsers(currentPage, pageSize, filter).then((response) => {
            setUsers(response);
        });
    }

    useEffect(() => {
        setSearchParams({page: currentPage, page_size: pageSize});
        const filter = {
            first_name: filterName,
            last_name: filterSurname,
            talents: filterTalent,
            groups: filterGroup
        }
        getUsers(currentPage, pageSize, filter).then((response) => {
            setUsers(response);
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
                    users.map((user) => {
                        return <div key={user.user._id} className='visible-layout width-full' style={{minWidth: '0px', height: '230px'}}>
                            <div className='border-box height-full width-full' style={{padding: '30px 0 30px 0'}}>
                                <div className='flex-row flex-space border-box width-full height-full' style={{padding: '0 100px 0 60px', gap: '30px'}}>
                                    <div className='fit-width'>
                                        <div className='avatar-container'>
                                            <img className='width-full height-full' style={{objectFit: 'cover'}} alt='' src={user.user.avatar_uri}></img>
                                        </div>
                                    </div>
                                    <div className='flex-column flex-center height-full width-full' style={{gap: '5px'}}>
                                        <div className='flex-row flex-space width-full'>
                                            <div className='flex-column'>
                                                <div className='first-name-text'>{user.user.first_name}</div>
                                                <div className='last-name-text'>{user.user.last_name}</div>
                                            </div> 
                                            <div className='flex-column align-center flex-center' style={{gap: '5px'}}>
                                                <BigStarIcon
                                                    style={{
                                                        stroke: 'var(--primary-color)', 
                                                        fill: true ? 'var(--primary-color)' : 'none'
                                                    }}
                                                />
                                                <div className='stars-count'>{user.stars.length}</div>
                                            </div> 
                                        </div>
                                        <div className='flex-row flex-space width-full'>
                                            <div className='tertiary-info'>Впервые присоединился</div>
                                            <div className='tertiary-info'>{user.user.creation_date}</div>
                                        </div>
                                        <div className='flex-row flex-space width-full'>
                                            <div className='tertiary-info'>Последнее изменение</div>
                                            <div className='tertiary-info'>{user.user.last_edit_date}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    })
                }
            </Pagination>
            <div className='flex-column fit-width' style={{paddingTop: '80px', gap: '20px'}}>
                <div className='visible-layout flex-column flex-center align-start' style={{padding: '20px', gap: '12px', width: '340px'}}>
                    <div className='caption'>Фильтрация</div>
                    <CustomTextField sx={{width: '100%'}} label="Имя" value={filterName} onChange={(event) => {setFilterName(event.target.value)}}/>
                    <CustomTextField sx={{width: '100%'}} label="Фамилия" value={filterSurname} onChange={(event) => {setFilterSurname(event.target.value)}}/>
                    <CustomTextField sx={{width: '100%'}} label="Талант" value={filterTalent} onChange={(event) => {setFilterTalent(event.target.value)}}/>
                    <CustomTextField sx={{width: '100%'}} label="Группа" value={filterGroup} onChange={(event) => {setFilterGroup(event.target.value)}}/>
                    <CustomButton variant='contained' sx={{alignSelf: 'end'}} onClick={handleFilter}>Применить</CustomButton>
                </div>
            </div>
        </div>
    </>;
}
