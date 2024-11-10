import './Pagination.css';

import Button from '@mui/material/Button';

export default function Pagination(props) {

    return <>
        <div className='flex-column width-full' style={{gap: '20px'}}>
            <div className='flex-row width-full flex-space'>
                <Button variant='contained'
                    onClick={props.onPreviousClick}
                >Previous</Button>
                <div>{props.pageNumber}</div>
                <Button variant='contained'
                    onClick={props.onNextClick}
                >Next</Button>
            </div>
            <div className='flex-column width-full' style={{gap: '10px'}}>
                {
                    props.children
                }
            </div>
        </div>
    </>;
}
