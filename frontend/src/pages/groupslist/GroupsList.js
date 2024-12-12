import './GroupsList.css';

import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from "react-router-dom";
import Pagination from '../components/pagination/Pagination.js';
import { CustomTextField, CustomButton, CustomDatePicker } from '../components/CustomMuiComponents.js';
import Button from '@mui/material/Button';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { getGroups, createGroup } from '../../requests/Requests.js';

import { ReactComponent as BigStarIcon } from './assets/big-star.svg';

export default function GroupsList(props) {

    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useSearchParams();

    const pageSize = 3;
    const [totalPages, setTotalPages] = useState(1);
    const [currentPage, setCurrentPage] = useState(1);
    const [groups, setGroups] = useState([]);

    const [newGroupName, setNewGroupName] = useState('');

    const [filterGroupName, setFilterGroupName] = useState('');
    const [filterGroupGenre, setFilterGroupGenre] = useState('');
    const [filterStarsFrom, setFilterStarsFrom] = useState('');
    const [filterStarsTo, setFilterStarsTo] = useState('');
    const [filterChangeDateFrom, setFilterChangeDateFrom] = useState('');
    const [filterChangeDateTo, setFilterChangeDateTo] = useState('');
    const [filterCreateDateFrom, setFilterCreateDateFrom] = useState('');
    const [filterCreateDateTo, setFilterCreateDateTo] = useState('');
    const [filterGroupMembers, setFilterGroupMembers] = useState('');

    const handleFilter = (event) => {
        const filter = {
            name: filterGroupName,
            genre: filterGroupGenre,
            from_stars: filterStarsFrom,
            to_stars: filterStarsTo,
            from_date: filterChangeDateFrom,
            to_date: filterChangeDateTo,
            from_creation: filterCreateDateFrom,
            to_creation: filterCreateDateTo,
            participant: filterGroupMembers
        };

        getGroups(currentPage, pageSize, filter).then((response) => {
            setGroups(response.group_list);
        });
    }

    const handleCreateGroup = (event) => {
        createGroup(newGroupName)
            .then(response => {
                navigate(0);
            })
            .catch(error => {
                toast('Введенные данные не соответствуют требованиям!');
            })
    }

    useEffect(() => {
        setSearchParams({page: currentPage, page_size: pageSize});

        const filter = {
            name: filterGroupName,
            genre: filterGroupGenre,
            from_stars: filterStarsFrom,
            to_stars: filterStarsTo,
            from_date: filterChangeDateFrom,
            to_date: filterChangeDateTo,
            from_creation: filterCreateDateFrom,
            to_creation: filterCreateDateTo,
            participant: filterGroupMembers
        };

        getGroups(currentPage, pageSize, filter).then((response) => {
            setGroups(response.group_list);
            setTotalPages(Math.ceil(response.count / pageSize));
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
        if (currentPage === totalPages) {
            toast('Ты уже на последней странице!'); 
            return;
        }
        setCurrentPage(currentPage + 1);
    }

    return <>
        <ToastContainer></ToastContainer>
        <div className='flex-row width-full' style={{gap: '20px'}}>
            <Pagination
                pageNumber={currentPage}
                totalPages={totalPages}
                onPreviousClick={handlePreviousClick}
                onNextClick={handleNextClick}
            >
                {
                    groups.map((group) => {
                        return <div key={group.group._id} className='visible-layout width-full' style={{minWidth: '0px', height: '230px'}}>
                            <div className='border-box height-full width-full' style={{padding: '30px 0 30px 0'}}>
                                <div className='flex-row flex-space border-box width-full height-full' style={{padding: '0 100px 0 60px', gap: '30px'}}>
                                    <div className='fit-width'>
                                        <div className='avatar-container'>
                                            <img className='width-full height-full' style={{objectFit: 'cover'}} alt='' src={group.group.avatar_uri}></img>
                                        </div>
                                    </div>
                                    <div className='flex-column flex-center height-full width-full' style={{gap: '5px'}}>
                                        <div className='flex-row flex-space width-full'>
                                            <div className='flex-column'>
                                                <div className='first-name-text'>{group.group.name}</div>
                                            </div> 
                                            <div className='flex-column align-center flex-center' style={{gap: '5px'}}>
                                                <BigStarIcon
                                                    style={{
                                                        stroke: 'var(--primary-color)', 
                                                        fill: true ? 'var(--primary-color)' : 'none'
                                                    }}
                                                />
                                                <div className='stars-count'>{group.stars.length}</div>
                                            </div> 
                                        </div>
                                        <div className='flex-row flex-space width-full'>
                                            <div className='tertiary-info'>Жанры</div>
                                            <div className='tertiary-info'>{JSON.stringify(group.group.genres)}</div>
                                        </div>
                                        <div className='flex-row flex-space width-full'>
                                            <div className='tertiary-info'>Последнее изменение</div>
                                            <div className='tertiary-info'>{group.group.last_edit_date}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    })
                }
            </Pagination>
            <div className='flex-column fit-width' style={{paddingTop: '80px', gap: '20px'}}>
                <div className='visible-layout flex-column flex-center align-start' style={{padding: '20px', gap: '12px', width: '340px', maxWidth: '340px'}}>
                    <div className='caption'>Создать группу</div>
                    <CustomTextField sx={{width: '100%'}} label="Название" variant="outlined" value={newGroupName} onChange={(event) => setNewGroupName(event.target.value)}/>
                    <CustomButton variant="contained" sx={{alignSelf: 'end'}} onClick={handleCreateGroup}>Создать</CustomButton>
                </div>
                <div className='visible-layout flex-column flex-center align-start' style={{padding: '20px', gap: '12px', width: '340px'}}>
                    <div className='caption'>Фильтрация</div>
                    <div className='caption' style={{fontSize: '15px', fontWeight: 'normal'}}>Название</div>
                    <CustomTextField sx={{width: '100%'}} label="Название" value={filterGroupName} onChange={(event) => setFilterGroupName(event.target.value)}/>
                    <div className='caption' style={{fontSize: '15px', fontWeight: 'normal'}}>Жанр</div>
                    <CustomTextField sx={{width: '100%'}} label="Жанр" value={filterGroupGenre} onChange={(event) => setFilterGroupGenre(event.target.value)}/>
                    <div className='caption' style={{fontSize: '15px', fontWeight: 'normal'}}>Участник</div>
                    <CustomTextField sx={{width: '100%'}} label="Участник" value={filterGroupMembers} onChange={(event) => setFilterGroupMembers(event.target.value)}/>
                    <div className='caption' style={{fontSize: '15px', fontWeight: 'normal'}}>Число звезд</div>
                    <div
                        className='flex-row width-full flex-space'
                        style={{gap: '5px'}}
                    >
                        <CustomTextField type="number" label="От" value={filterStarsFrom} onChange={(event) => setFilterStarsFrom(event.target.value)}/>
                        <CustomTextField type="number" label="До" value={filterStarsTo} onChange={(event) => setFilterStarsTo(event.target.value)}/>

                    </div>
                    <div className='caption' style={{fontSize: '15px', fontWeight: 'normal'}}>Дата изменения</div>
                    <div
                        className='flex-column width-full flex-space'
                        style={{gap: '5px'}}
                    >
                        <CustomDatePicker label="От" onChange={(event) => setFilterChangeDateFrom(event)}></CustomDatePicker>
                        <CustomDatePicker label="До" onChange={(event) => setFilterChangeDateTo(event)}></CustomDatePicker>
                    </div>
                    <div className='caption' style={{fontSize: '15px', fontWeight: 'normal'}}>Дата создания</div>
                    <div
                        className='flex-column width-full flex-space'
                        style={{gap: '5px'}}
                    >
                        <CustomDatePicker label="От" onChange={(event) => setFilterCreateDateFrom(event)}></CustomDatePicker>
                        <CustomDatePicker label="До" onChange={(event) => setFilterCreateDateTo(event)}></CustomDatePicker>
                    </div>
                    <CustomButton variant="contained" sx={{alignSelf: 'end'}} onClick={handleFilter}>Примерить</CustomButton>
                </div>
            </div>
        </div>
    </>;
}
