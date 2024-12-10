import './Statistic.css';

import React, { useState, useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Button from '@mui/material/Button';

import { importData, exportData } from '../../requests/Requests.js';

import { CustomButton, VisuallyHiddenInput } from '../../pages/components/CustomMuiComponents.js';

export default function Statistic(props) {

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        console.log(file);
        const formData = new FormData();
        formData.append('file', file);
        importData(formData).then((response) => {
            console.log(response);
        });
    }

    const handleFileDownload = (event) => {
        exportData();
    } 

    return <>
        <div
            className='width-full height-full flex-column border-box'
            style={{
                padding: '30px 0 0 0'
            }}
        >
            <div
                className='width-full flex-row border-box visible-layout flex-space align-center'
                style={{
                    padding: '0 30px 0 30px',
                    height: '50px'
                }}
            >
                <div>

                </div>

                <div
                    className='flex-row'
                    style={{
                        gap: '10px'
                    }}
                >
                    <CustomButton
                        component='label'
                        sx={{
                            width: '142px',
                            height: '30px',
                            fontSize: '10px'
                        }}
                    >
                        Импортировать данные
                        <VisuallyHiddenInput
                            type="file"
                            onChange={handleFileUpload}
                        />
                    </CustomButton>
                    <CustomButton
                        sx={{
                            width: '142px',
                            height: '30px',
                            fontSize: '10px'
                        }}
                        onClick={handleFileDownload}
                    >Экспортировать данные</CustomButton>
                </div>
            </div>
        </div> 
    </>;
}
