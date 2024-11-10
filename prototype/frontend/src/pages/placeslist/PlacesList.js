import './PlacesList.css';

import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from "react-router-dom";
import Pagination from '../components/pagination/Pagination.js';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { getPlaces, createPlace } from '../../requests/Requests.js';

export default function PlacesList(props) {

    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useSearchParams();

    const pageSize = 3; const [currentPage, setCurrentPage] = useState(1);
    const [places, setPlaces] = useState([]);

    const [newPlaceName , setNewPlaceName] = useState('');
    const [newPlaceType , setNewPlaceType] = useState('');
    const [newPlaceAddress, setNewPlaceAddress] = useState('');
    const [newPlaceNumber, setNewPlaceNumber] = useState('');

    const handleCreateGroup = (event) => {
        createPlace(newPlaceName, newPlaceType, newPlaceAddress, newPlaceNumber)
            .then(response => {
                navigate(0);
            })
            .catch(error => {
                toast('Введенные данные не соответствуют требованиям!');
            })
    }

    useEffect(() => {
        setSearchParams({page: currentPage, page_size: pageSize});
        getPlaces(currentPage, pageSize).then((response) => {
            setPlaces(response);
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
                    places.map((place) => {
                        return <div key={place._id} className='visible-layout width-full' style={{minWidth: '0px', height: '230px'}}>
                            <div className='border-box height-full width-full' style={{padding: '30px 0 30px 0'}}>
                                <div className='flex-row flex-space border-box width-full height-full' style={{padding: '0 100px 0 60px', gap: '30px'}}>
                                    <div className='fit-width'>
                                        <div className='avatar-container'>
                                            <img className='width-full height-full' style={{objectFit: 'cover'}} alt='' src={place.avatar_uri}></img>
                                        </div>
                                    </div>
                                    <div className='flex-column flex-center height-full width-full' style={{gap: '5px'}}>
                                        <div className='flex-row flex-space width-full'>
                                            <div className='flex-column'>
                                                <div className='first-name-text'>{place.name}</div>
                                            </div> 
                                        </div>
                                        <div className='flex-row width-full'>
                                            <div className='tertiary-info' style={{color: 'var(--text-color)'}}>{place.type}</div>
                                        </div>
                                        <div className='flex-row flex-space width-full'>
                                            <div className='tertiary-info'>Адрес</div>
                                            <div className='tertiary-info'>{place.address}</div>
                                        </div>
                                        <div className='flex-row flex-space width-full'>
                                            <div className='tertiary-info'>Контактный номер</div>
                                            <div className='tertiary-info'>{place.phone_number}</div>
                                        </div>
                                        <div className='flex-row flex-space width-full'>
                                            <div className='tertiary-info'>Оборудование</div>
                                            <div className='tertiary-info'>{JSON.stringify(place.equipment)}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    })
                }
            </Pagination>
            <div className='fit-width'>
                <div className='visible-layout flex-column flex-center' style={{padding: '20px', gap: '10px'}}>
                    <TextField id="outlined-basic" label="Название" variant="outlined" value={newPlaceName} onChange={(event) => setNewPlaceName(event.target.value)}/>
                    <TextField id="outlined-basic" label="Тип" variant="outlined" value={newPlaceType} onChange={(event) => setNewPlaceType(event.target.value)}/>
                    <TextField id="outlined-basic" label="Адрес" variant="outlined" value={newPlaceAddress} onChange={(event) => setNewPlaceAddress(event.target.value)}/>
                    <TextField id="outlined-basic" label="Контактный номер" variant="outlined" value={newPlaceNumber} onChange={(event) => setNewPlaceNumber(event.target.value)}/>
                    <Button variant="contained" onClick={handleCreateGroup}>Создать</Button>
                </div>
            </div>
        </div>
    </>;
}
