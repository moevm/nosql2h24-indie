import './GroupsList.css';

import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from "react-router-dom";
import Pagination from '../components/pagination/Pagination.js';
import { CustomTextField, CustomButton } from '../components/CustomMuiComponents.js';
import Button from '@mui/material/Button';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { getGroups, createGroup } from '../../requests/Requests.js';

import { ReactComponent as BigStarIcon } from './assets/big-star.svg';

export default function GroupsList(props) {

    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useSearchParams();

    const pageSize = 3;
    const [currentPage, setCurrentPage] = useState(1);
    const [groups, setGroups] = useState([]);

    const [newGroupName, setNewGroupName] = useState('');

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
        getGroups(currentPage, pageSize).then((response) => {
            setGroups(response);
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
            <div className='fit-width'>
                <div className='visible-layout flex-column flex-center align-end' style={{padding: '20px', gap: '10px'}}>
                    <CustomTextField id="outlined-basic" label="Название" variant="outlined" value={newGroupName} onChange={(event) => setNewGroupName(event.target.value)}/>
                    <CustomButton variant="contained" onClick={handleCreateGroup}>Создать</CustomButton>
                </div>
            </div>
        </div>
    </>;
}
