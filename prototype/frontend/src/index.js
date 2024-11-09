import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import Footer from './pages/components/footer/Footer.js';
import UserProfile from './pages/userprofile/UserProfilePage.js';
import GroupProfile from './pages/groupprofile/GroupProfilePage.js';

const router = createBrowserRouter([
    {
        path: '/',
        element: <Footer></Footer>,
        children: [
            {
                path: '/',
                element: <div>Hello world!</div>,
            },
            {
                path: '/users',
                element: <div>Users list</div> 
            },
            {
                path: '/users/:userId',
                element: <UserProfile></UserProfile> 
            },
            {
                path: '/groups',
                element: <div>Groups list</div> 
            },
            {
                path: '/groups/:groupId',
                element: <GroupProfile></GroupProfile> 
            },
            {
                path: '/places',
                element: <div>Places list</div> 
            },
            {
                path: '/announcements',
                element: <div>Announcements list</div> 
            },
            {
                path: 'statistic',
                element: <div>Statistic</div>
            },
            {
                path: 'auth',
                element: <div>Authentification/Login</div>
            }
        ]
    }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <RouterProvider router={router}/>
    </React.StrictMode>
);
