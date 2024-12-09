import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import Footer from './pages/components/footer/Footer.js';
import UserProfile from './pages/userprofile/UserProfilePage.js';
import GroupProfile from './pages/groupprofile/GroupProfilePage.js';
import Autorization from './pages/authorization/Authorization.js';
import AnnouncementsList from './pages/announcementslist/AnnouncementsList.js';
import UsersList from './pages/userslist/UsersList.js';
import GroupsList from './pages/groupslist/GroupsList.js';
import PlacesList from './pages/placeslist/PlacesList.js';
import Statistic from './pages/statistic/Statistic.js';

const router = createBrowserRouter([
    {
        path: '/',
        element: <Footer></Footer>,
        children: [
            {
                path: '/auth',
                element: <Autorization></Autorization>,
            },
            {
                path: '/users',
                element: <UsersList></UsersList> 
            },
            {
                path: '/users/:userId',
                element: <UserProfile></UserProfile> 
            },
            {
                path: '/groups',
                element: <GroupsList></GroupsList> 
            },
            {
                path: '/groups/:groupId',
                element: <GroupProfile></GroupProfile> 
            },
            {
                path: '/places',
                element: <PlacesList></PlacesList> 
            },
            {
                path: '/announcements',
                element: <AnnouncementsList></AnnouncementsList> 
            },
            {
                path: '/statistic',
                element: <Statistic></Statistic> 
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
