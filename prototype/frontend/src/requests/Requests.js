
const protocol = 'http';
const host = 'localhost';
const port = '8000';

const baseUrl = `${protocol}://${host}:${port}/api`;

export function getUser(userId) {
    return fetch(`${baseUrl}/user/${userId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json());
}

export function postUserAnnouncement(userId, announcement) {
    return fetch(`${baseUrl}/user_announcement`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: userId, announcement: announcement })
        })
        .then(response => response.json());
}
