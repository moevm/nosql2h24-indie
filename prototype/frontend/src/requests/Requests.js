
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

export function getUserStarred(sourceUserId, destinationUserId) {
    return fetch(`${baseUrl}/get_user_star?source_user_id=${sourceUserId}&dest_user_id=${destinationUserId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json());
}

export function addStarToUser(sourceUserId, destinationUserId) {
    return fetch(`${baseUrl}/user_star`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ from: sourceUserId, to: destinationUserId })
        })
        .then(response => response.json());
}
