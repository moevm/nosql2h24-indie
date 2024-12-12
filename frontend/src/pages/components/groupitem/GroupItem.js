import './GroupItem.css';

import React, { useState, useEffect, useContext } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import { Dropdown } from '../CustomMuiComponents.js';

import SelectTag from '../selecttag/SelectTag.js';

import Select from '@mui/material/Select';



export default function GroupItem(props) {

    return <>
        <div
            className="visible-layout border-box flex-row width-full"
            style={{
                height: 'fit-content',
                padding: '14px',
                gap: '20px'
            }}
        >
            <div className='fit-width'>
                <div className='avatar-container' style={{width: '80px', height: '80px'}}>
                    <img className='width-full height-full' style={{objectFit: 'cover'}} alt='' src={props.avatar_uri}></img>
                </div>
            </div>
            <div
                className='width-full flex-column'
                style={{
                    gap: '10px'
                }}
            >
                <div className='important-text'>
                    {props.name}
                </div>
                <Dropdown
                    label="Жанры"
                >
                    {props.genres.map((gener) => {
                        return <div>{gener}</div>;
                    })}
                </Dropdown>
                {JSON.stringify(props)}
            </div>
            <div className='fit-width'>
                <div
                    className='flex-column'
                >
                    <div className='text'>
                    </div>
                    <div className='text'>
                    </div>
                </div>
            </div>
        </div>
    </>;
}
