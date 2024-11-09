import './UserProfilePage.css';

import React, { useState } from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';

import TalentDisplay from '../components/talentdisplay/TalentDisplay.js';
import UserGroupInfo from '../components/usergroupinfo/UserGroupInfo.js';
import PostAnnouncement from '../components/postannouncement/PostAnnouncement.js';
import Announcement from '../components/announcement/Announcement.js';

import { ReactComponent as BigStarIcon } from './big-star.svg';

const CustomButton = styled(Button)(() => ({
    width: '120px',
    height: '40px',

    backgroundColor: 'var(--primary-color)',
    borderRadius: '10px',

    color: 'var(--contrast-text-color)',
    fontSize: '10px',
    fontWeight: 'normal',
    textTransform: 'none'
}));

export default function UserProfile(props) {

    const [profileStarred, setProfileStarred] = useState(false);

    return <>
        <div className='border-box flex-column width-full height-full' style={{boxSizing: 'border-box', paddingTop: '70px', gap: '40px'}}>
            <div className='flex-row flex-space width-full' style={{height: '230px', gap: '30px'}}>
                <div className='visible-layout height-full width-full' style={{minWidth: '0px'}}>
                    <div className='border-box height-full width-full' style={{padding: '30px 0 30px 0'}}>
                        <div className='flex-row flex-space border-box width-full height-full' style={{padding: '0 100px 0 60px', gap: '30px'}}>
                            <div className='fit-width'>
                                <div className='avatar-container'>
                                    <img className='width-full height-full' style={{objectFit: 'cover'}} alt='' src='https://preview.redd.it/young-thom-yorke-v0-1d3qmko89jsc1.jpg?width=738&format=pjpg&auto=webp&s=cae24d549db41a16d23da2f40343fc77035be5cd'></img>
                                </div>
                            </div>
                            <div className='flex-column flex-center height-full width-full' style={{gap: '5px'}}>
                                <div className='flex-row flex-space width-full'>
                                    <div className='flex-column'>
                                        <div className='first-name-text'>Томас</div>
                                        <div className='last-name-text'>Йорк</div>
                                    </div> 
                                    <div className='flex-column align-center flex-center' style={{gap: '5px'}}>
                                        <BigStarIcon
                                            style={{
                                                stroke: 'var(--primary-color)', 
                                                fill: profileStarred ? 'var(--primary-color)' : 'none'
                                            }}
                                            onClick={(event) => {
                                                setProfileStarred(!profileStarred);
                                            }}
                                        />
                                        <div className='stars-count'>1k+</div>
                                    </div> 
                                </div>
                                <div className='flex-row flex-space width-full'>
                                    <div className='tertiary-info'>Впервые присоединился</div>
                                    <div className='tertiary-info'>01.01.2020</div>
                                </div>
                                <div className='flex-row flex-space width-full'>
                                    <div className='tertiary-info'>Последнее изменение</div>
                                    <div className='tertiary-info'>01.01.2020</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className='visible-layout height-full' style={{minWidth: '340px'}}>
                    <div className='border-box flex-row width-full height-full' style={{padding: '0 35px 0 35px'}}>
                        <div className='border-box flex-column width-full height-full' style={{padding: '25px 0 25px 0', gap: '10px'}}>
                            <div className='fit-height'>
                                <div className='caption'>Таланты</div>
                            </div>
                            <div className='scroll-column' style={{gap: '10px', paddingRight: '10px'}}>
                                <TalentDisplay
                                    talent='vocal'
                                />
                                <TalentDisplay
                                    talent='electric-guitar'
                                />
                                <TalentDisplay
                                    talent='acoustic-guitar'
                                />
                                <TalentDisplay
                                    talent='drums'
                                />
                                <TalentDisplay
                                    talent='bass'
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className='flex-row width-full height-full' style={{gap: '30px'}}>
                <div className='flex-column width-full heigth-full' style={{gap: '20px'}}>
                    <div className='border-box visible-layout flex-column width-full' style={{minWidth: '600px', height: '80px', padding: '16px 0 16px 0'}}>
                        <div className='border-box flex-row flex-space width-full height-full align-center' style={{padding: '0 20px 0 40px'}}>
                            <div className='caption'>
                                Действия
                            </div>
                            <CustomButton className='actions-button' variant='contained'>
                                Пригласить в группу
                            </CustomButton>
                        </div>
                    </div>
                    <PostAnnouncement 

                    />
                    <div className='width-full height-full' style={{position: 'relative'}}>
                        <div className='scroll-column' style={{gap: '20px'}}>
                            <Announcement 
                                authorName='Томас'
                                tag='Концерт'
                                date='1 час назад'
                                content='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eget libero eget odio 
                                        elementum efficitur ac ac ligula. In sed dui vitae mauris elementum euismod eu a augue. 
                                        Aenean ullamcorper.'
                                starsAmount='1k+'
                            />
                        </div>
                    </div>
                </div>
                <div className='fit-width'>
                    <div className='visible-layout border-box flex-row' style={{width: '340px', height: '450px', padding: '0 35px 0 35px'}}>
                        <div className='border-box flex-column width-full height-full' style={{padding: '25px 0 40px 0', gap: '10px'}}>
                            <div className='caption'>Группы</div>
                            <div className='scroll-column' style={{gap: '15px', paddingRight: '15px'}}>
                                <UserGroupInfo
                                    group={{name: 'Радиолюбители', avatar_uri: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVfBzJ3q1OdwAUnScbjEdYUh8psz24q0meDw&s'}}
                                    joinDate={'01.01.2020'}
                                />
                                <UserGroupInfo
                                    group={{name: 'Улыбка', avatar_uri: 'https://yt3.googleusercontent.com/aCf8WKRR9eqx0GhLLLoaDCJKRv-udsfJtX0K4xnrBBJeKPIf5jIGbzKE4kZ5lZSRVzvmjZjyCQ=s900-c-k-c0x00ffffff-no-rj'}}
                                    joinDate={'01.01.2020'}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </>;
};
