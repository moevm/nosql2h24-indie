import './PlacesList.css';

import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from "react-router-dom";
import Pagination from '../components/pagination/Pagination.js';
import { CustomButton, CustomTextField } from '../components/CustomMuiComponents.js';
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

    const [filterPlaceName, setFilterPlaceName] = useState('');
    const [filterPlaceType, setFilterPlaceType] = useState('');
    const [filterPlaceAddress, setFilterPlaceAddress] = useState('');
    const [filterPlaceNumber, setFilterPlaceNumber] = useState('');
    const [filterPlaceEquipment, setFilterPlaceEquipment] = useState('');

    const handleCreateGroup = (event) => {
        createPlace(newPlaceName, newPlaceType, newPlaceAddress, newPlaceNumber)
            .then(response => {
                navigate(0);
            })
            .catch(error => {
                toast('Введенные данные не соответствуют требованиям!');
            })
    }

    const handleFilter = (event) => {
        const filter = {
            name: filterPlaceName,
            type: filterPlaceType,
            address: filterPlaceAddress,
            number: filterPlaceNumber,
            equipment: filterPlaceEquipment
        }
        getPlaces(currentPage, pageSize, filter).then((response) => {
            setPlaces(response);
        });
    }

    useEffect(() => {
        setSearchParams({page: currentPage, page_size: pageSize});
        const filter = {
            name: filterPlaceName,
            type: filterPlaceType,
            address: filterPlaceAddress,
            number: filterPlaceNumber,
            equipment: filterPlaceEquipment
        }
        getPlaces(currentPage, pageSize, filter).then((response) => {
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
            <div className='flex-column fit-width' style={{paddingTop: '80px', gap: '20px'}}>
                <div className='visible-layout flex-column flex-center align-start' style={{padding: '20px', gap: '12px', width: '340px'}}>
                    <div className='caption'>Добавить место</div>
                    <CustomTextField sx={{width: '100%'}} label="Название" value={newPlaceName} onChange={(event) => setNewPlaceName(event.target.value)}/>
                    <CustomTextField sx={{width: '100%'}} label="Тип" value={newPlaceType} onChange={(event) => setNewPlaceType(event.target.value)}/>
                    <CustomTextField sx={{width: '100%'}} label="Адрес" value={newPlaceAddress} onChange={(event) => setNewPlaceAddress(event.target.value)}/>
                    <CustomTextField sx={{width: '100%'}} label="Контактный номер" value={newPlaceNumber} onChange={(event) => setNewPlaceNumber(event.target.value)}/>
                    <CustomButton sx={{alignSelf: 'end'}} variant="contained" onClick={handleCreateGroup}>Создать</CustomButton>
                </div>
                <div className='visible-layout flex-column flex-center align-start' style={{padding: '20px', gap: '12px', width: '340px'}}>
                    <div className='caption'>Фильтрация</div>
                    <CustomTextField sx={{width: '100%'}} label="Название" value={filterPlaceName} onChange={(event) => setFilterPlaceName(event.target.value)}/>
                    <CustomTextField sx={{width: '100%'}} label="Тип" value={filterPlaceType} onChange={(event) => setFilterPlaceType(event.target.value)}/>
                    <CustomTextField sx={{width: '100%'}} label="Адрес" value={filterPlaceAddress} onChange={(event) => setFilterPlaceAddress(event.target.value)}/>
                    <CustomTextField sx={{width: '100%'}} label="Контактный номер" value={filterPlaceNumber} onChange={(event) => setFilterPlaceNumber(event.target.value)}/>
                    <CustomTextField sx={{width: '100%'}} label="Оборудование" value={filterPlaceEquipment} onChange={(event) => setFilterPlaceEquipment(event.target.value)}/>
                    <CustomButton variant="contained" sx={{alignSelf: 'end'}} onClick={handleFilter}>Примерить</CustomButton>
                </div>
            </div>
        </div>
    </>;
}
