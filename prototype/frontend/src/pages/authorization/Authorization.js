import './Authorization.css';

import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { UserContext } from '../../contexts/UserContext.js';
import { authorization, registration } from '../../requests/Requests.js';

export default function Authorization(props) {

    const navigate = useNavigate();

    const [lastName, setLastName] = useState('');
    const [firstName, setFirstName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');

    const handleRegister = () => {
        if (password === repeatPassword) {
            registration(firstName, lastName, email, password)
                .then(response => {
                    localStorage.setItem('userId', response._key);
                    setAuthentifiedUserId(response._key);
                    navigate(`/users/${response._key}`);
                })
                .catch(error => {
                    toast('Введенные данные не соответствуют требованиям!');
                })
        } else {
            toast('Пароли не совпадают!');
        }


    }

    const [authentifiedUserId, setAuthentifiedUserId] = useContext(UserContext);
    const [loginEmail, setLoginEmail] = useState('');
    const [loginPassword, setLoginPassword] = useState('');

    const handleLogin = () => {
        authorization(loginEmail, loginPassword)
            .then(response => {
                if (response.code === 200) {
                    localStorage.setItem('userId', response.body._key);
                    setAuthentifiedUserId(response.body._key);
                    navigate('/announcements');
                } else {
                    toast("Неверные данные!");
                }
            })
    }


    return <>
        <ToastContainer></ToastContainer>
        <div className='flex-row width-full' style={{ gap: '20px' }}>
            <div className='flex-column' style={{ gap: '20px' }}>
                <div>
                    Регистрация
                </div>
                <div className='flex-column' style={{ gap: '10px' }}>

                    <TextField id="outlined-basic" label="Фамилия" variant="outlined" value={lastName} onChange={(event) => { setLastName(event.target.value) }}/>
                    <TextField id="outlined-basic" label="Имя" variant="outlined" value={firstName} onChange={(event) => { setFirstName(event.target.value) }} />
                    <TextField id="outlined-basic" label="email" variant="outlined" value={email} onChange={(event) => { setEmail(event.target.value) }} />
                    <TextField id="outlined-basic" label="Пароль" variant="outlined" value={password} onChange={(event) => { setPassword(event.target.value) }} />
                    <TextField id="outlined-basic" label="Повторите пароль" variant="outlined" value={repeatPassword} onChange={(event) => { setRepeatPassword(event.target.value) }} />
                    <Button variant="contained" onClick={handleRegister}>Регистрация</Button>

                </div>
            </div>
            <div className='flex-column' style={{ gap: '20px' }}>
                <div>
                    Авторизация
                </div>
                <div className='flex-column' style={{ gap: '10px' }}>

                    <TextField id="outlined-basic" label="email" variant="outlined" value={loginEmail} onChange={(event) => { setLoginEmail(event.target.value) }} />
                    <TextField id="outlined-basic" label="Пароль" variant="outlined" value={loginPassword} onChange={(event) => { setLoginPassword(event.target.value) }} />
                    <Button variant="contained" onClick={handleLogin}>Вход</Button>

                </div>

            </div>
        </div>
    </>;
}
