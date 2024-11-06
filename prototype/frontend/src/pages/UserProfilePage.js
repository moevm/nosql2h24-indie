import './UserProfilePage.css';
import { ReactComponent as BigStarIcon } from './big-star.svg';
import { ReactComponent as VocalIcon } from './vocal.svg';
import { ReactComponent as ElectricGuitarIcon } from './electric-guitar.svg';
import { ReactComponent as AcousticGuitarIcon } from './acoustic-guitar.svg';
import React, { useState } from 'react';

export default function UserProfile(props) {

    const [profileStarred, setProfileStarred] = useState(false);

    return <>
        <div className='flex-column width-full height-full' style={{boxSizing: 'border-box', paddingTop: '70px', gap: '40px'}}>
            <div className='flex-row flex-space width-full' style={{height: '230px', gap: '30px'}}>
                <div className='user-info-layout height-full width-full'>
                    <div className='border-box height-full width-full' style={{padding: '30px 0 30px 0'}}>
                        <div className='flex-row flex-space border-box width-full height-full' style={{padding: '0 100px 0 60px', gap: '30px'}}>
                            <div className='fit-width'>
                                <div className='avatar-container'>
                                    <img className='width-full height-full' style={{objectFit: 'cover'}} src='https://preview.redd.it/young-thom-yorke-v0-1d3qmko89jsc1.jpg?width=738&format=pjpg&auto=webp&s=cae24d549db41a16d23da2f40343fc77035be5cd'></img>
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
                <div className='talents-layout height-full' style={{minWidth: '340px'}}>
                    <div className='border-box flex-row width-full height-full' style={{padding: '0 35px 0 35px'}}>
                        <div className='border-box flex-column width-full height-full' style={{padding: '25px 0 25px 0', gap: '10px'}}>
                            <div className='fit-height'>
                                <div className='caption'>Таланты</div>
                            </div>
                            <div className='scroll-column' style={{gap: '10px', paddingRight: '10px'}}>
                                <div className='flex-row align-center' style={{gap: '5px'}}>
                                    <VocalIcon style={{width: '30px', height: '30px', fill: 'var(--primary-color)'}} />
                                    <div className='talent-name'>Вокал</div>
                                </div>
                                <div className='flex-row align-center' style={{gap: '5px'}}>
                                    <ElectricGuitarIcon style={{width: '30px', height: '30px', fill: 'var(--primary-color)', stroke: 'var(--primary-color)'}} />
                                    <div className='talent-name'>Электрогитара</div>
                                </div>
                                <div className='flex-row align-center' style={{gap: '5px'}}>
                                    <AcousticGuitarIcon style={{width: '30px', height: '30px', fill: 'var(--primary-color)'}} />
                                    <div className='talent-name'>Акустическая гитара</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </>;
};
