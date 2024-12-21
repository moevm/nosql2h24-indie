import React, { useState, useEffect } from 'react';

import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';

import UserFilter from '../filters/UserFilter.js';
import GroupFilter from '../filters/GroupFilter.js';
import PlaceFilter from '../filters/PlaceFilter.js';
import AnnouncementFilter from '../filters/AnnouncementFilter.js';

export default function Diagrams(props) {

    const [entity, setEntity] = useState('user');

    const renderFilter = (event) => {
        switch (entity) {
            case 'user':
                return <UserFilter
                    onSubmit={(filter) => {
                        console.log(filter);
                    }}
                />
            case 'group':
                return <GroupFilter 
                    onSubmit={(filter) => {
                        console.log(filter);
                    }}
                />
            case 'place':
                return <PlaceFilter 
                    onSubmit={(filter) => {
                        console.log(filter);
                    }}
                />
            case 'announcement':
                return <AnnouncementFilter 
                    onSubmit={(filter) => {
                        console.log(filter);
                    }}
                />
        }
    }

    return <>
        <div
            className='width-full flex-row border-box'
            style={{
                gap: '10px'
            }}
        >
            <div
                className='width-full border-box visible-layout'
                style={{
                    height: '400px'
                }}
            >

            </div>
            <div
                className='flex-column border-box fit-width'
                style={{
                    gap: '10px'
                }}
            >
                <div
                    className='visible-layout border-box'
                    style={{
                        width: '380px',
                        padding: '10px',
                    }}
                >
                    <div
                        className='caption'
                    >
                        Выберите сущность
                    </div>
                    <RadioGroup
                        value={entity}
                        onChange={(event) => {
                            setEntity(event.target.value)
                        }}
                    >
                        <FormControlLabel value="user" control={<Radio />} label="Пользователи"
                            sx={{
                                '& .MuiFormControlLabel-label': {
                                    color: 'var(--text-color)'
                                },
                                '& .MuiSvgIcon-root': {
                                    color: 'var(--primary-color)'
                                }
                            }}
                        />
                        <FormControlLabel value="group" control={<Radio />} label="Группы" 
                            sx={{
                                '& .MuiFormControlLabel-label': {
                                    color: 'var(--text-color)'
                                },
                                '& .MuiSvgIcon-root': {
                                    color: 'var(--primary-color)'
                                }
                            }}
                        />
                        <FormControlLabel value="place" control={<Radio />} label="Места" 
                            sx={{
                                '& .MuiFormControlLabel-label': {
                                    color: 'var(--text-color)'
                                },
                                '& .MuiSvgIcon-root': {
                                    color: 'var(--primary-color)'
                                }
                            }}
                        />
                        <FormControlLabel value="announcement" control={<Radio />} label="Объявления" 
                            sx={{
                                '& .MuiFormControlLabel-label': {
                                    color: 'var(--text-color)'
                                },
                                '& .MuiSvgIcon-root': {
                                    color: 'var(--primary-color)'
                                }
                            }}
                        />
                    </RadioGroup>
                </div>
                {renderFilter()}
            </div>
        </div>
    </>;
}
