import { styled } from '@mui/material/styles';

import Button from '@mui/material/Button';

import Tab from '@mui/material/Tab';
import TabList from '@mui/lab/TabList';

import TextField from '@mui/material/TextField';

export const CustomButton = styled(Button)(() => ({
    width: '120px',
    height: '40px',

    backgroundColor: 'var(--primary-color)',
    borderRadius: '10px',

    color: 'var(--contrast-text-color)',
    fontSize: '16px',
    fontWeight: 'normal',
    textTransform: 'none'
}));

export const CustomTab = styled(Tab)(() => ({
    "&.Mui-selected": {
        color: 'var(--text-color)',
        fontWeight: 'bold'
    },
    color: 'var(--text-color)',
    borderColorBottom: 'red'
}));

export const CustomTabList = styled(TabList)(() => ({
    "& .MuiTabs-indicator": {
        backgroundColor: 'var(--primary-color)'
    }

}));

export const CustomTextField = styled(TextField)(() => ({
    "& input": {
        boxSizing: 'border-box',
        height: '23px',
        fontSize: '16px',
        padding: '0 10px',
        backgroundColor: 'var(--text-color)',
        color: 'var(--base-color)',
        borderRadius: '10px',
    },
    "& fieldset": {
        border: 'none',
        color: 'red',
    },
    "& label.Mui-focused": {
        display: "none"
    },
    "& label.MuiFormLabel-filled": {
        display: "none"
    },
    "& label": {
        transform: 'translate(12px, 20%) scale(0.75)'
    }
}));

export const VisuallyHiddenInput = styled('input')({
    clip: 'rect(0 0 0 0)',
    clipPath: 'inset(50%)',
    height: 1,
    overflow: 'hidden',
    position: 'absolute',
    bottom: 0,
    left: 0,
    whiteSpace: 'nowrap',
    width: 1,
});
