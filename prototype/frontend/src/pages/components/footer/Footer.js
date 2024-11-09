import './Footer.css';

import React, { useState } from 'react';
import { NavLink, Outlet } from 'react-router-dom';

import { TagsContext } from '../../../contexts/TagsContext.js';

import { ReactComponent as AnnouncementsIcon } from './assets/announcements.svg';
import { ReactComponent as GroupsIcon } from './assets/groups.svg';
import { ReactComponent as UsersIcon } from './assets/users.svg';
import { ReactComponent as PlacesIcon } from './assets/places.svg';
import { ReactComponent as ProfileIcon } from './assets/profile.svg';
import { ReactComponent as StatisticIcon } from './assets/statistic.svg';

export default function Footer(props) {

    let checkActive = ({ isActive }) => {
        return isActive ? 'active' : 'unactive';
    }

    const [tags] = useState(['Концерт', 'Релиз']);

    return <>
        <div className='backdrop'></div>
        <div className='layout'>
            <div className='border-box width-full height-full' style={{position: 'relative', minWidth: '970px', paddingBottom: '160px'}}>
                <TagsContext.Provider value={tags}>
                    <Outlet></Outlet>
                </TagsContext.Provider>
                <div className='navbar flex-row flex-center'>
                    <div className='flex-row align-center' style={{gap: '40px'}}>
                        <NavLink to='/announcements' className={checkActive} style={{textDecoration: 'none'}}>
                            <div className='flex-column align-center'>
                                <AnnouncementsIcon style={{width: '48px', height: '46px'}} part='icon' />
                                <div className='icon-caption'>Объявления</div>
                            </div>
                        </NavLink>
                        <NavLink to='/groups' className={checkActive} style={{textDecoration: 'none'}}>
                            <div className='flex-column align-center'>
                                <GroupsIcon style={{width: '48px', height: '46px'}} part='icon'/>
                                <div className='icon-caption'>Группы</div>
                            </div>
                        </NavLink>
                        <NavLink to='/users' className={checkActive} style={{textDecoration: 'none'}}>
                            <div className='flex-column align-center'>
                                <UsersIcon style={{width: '48px', height: '46px'}} part='icon'/>
                                <div className='icon-caption'>Пользователи</div>
                            </div>
                        </NavLink>
                        <NavLink to='/places' className={checkActive} style={{textDecoration: 'none'}}>
                            <div className='flex-column align-center'>
                                <PlacesIcon style={{width: '48px', height: '46px'}} part='icon'/>
                                <div className='icon-caption'>Места</div>
                            </div>
                        </NavLink>
                        <NavLink to='/users/1' className={checkActive} style={{textDecoration: 'none'}}>
                            <div className='flex-column align-center'>
                                <ProfileIcon style={{width: '48px', height: '46px'}} part='icon'/>
                                <div className='icon-caption'>Профиль</div>
                            </div>
                        </NavLink>
                        <NavLink to='/statistic' className={checkActive} style={{textDecoration: 'none'}}>
                            <div className='flex-column align-center'>
                                <StatisticIcon style={{width: '48px', height: '46px'}} part='icon'/>
                                <div className='icon-caption'>Статистика</div>
                            </div>
                        </NavLink>
                    </div>
                </div>
            </div>
        </div>
    </>;
};
