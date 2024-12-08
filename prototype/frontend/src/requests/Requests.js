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

export function getAnnouncementStarred(sourceUserId, destinationAnnouncementId) {
    return fetch(`${baseUrl}/get_announcement_star?source_user_id=${sourceUserId}&dest_announcement_id=${destinationAnnouncementId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json());
}

export function addStarToAnnouncement(sourceUserId, destinationAnnouncementId) {
    return fetch(`${baseUrl}/star`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ from: sourceUserId, to:destinationAnnouncementId })
        })
        .then(response => response.json());
}

export function getTags() {
    return fetch(`${baseUrl}/static_all/?static_field=tags`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json());
}

export function authorization(email, password) {
    return fetch(`${baseUrl}/authorization`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email, password: password })
        })
        .then(response => response.json());
}

export function registration(firstName, lastName, email, password) {
    return fetch(`${baseUrl}/registration`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: firstName, surname: lastName, email: email, password: password })
        })
        .then(response => response.json());
}

export function getAnnouncements(page, pageSize) {
    return fetch(`${baseUrl}/announcement/${page}${pageSize}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json());
}

export function getUsers(page, pageSize) {
    return fetch(`${baseUrl}/users/${page}${pageSize}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json());
}

export function getGroups(page, pageSize) {
    return fetch(`${baseUrl}/groups/${page}${pageSize}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json());
}

export function getPlaces(page, pageSize) {
    return fetch(`${baseUrl}/places/${page}${pageSize}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json());
}

export function createGroup(groupName) {
    return fetch(`${baseUrl}/group`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: groupName })
        })
        .then(response => response.json());
} 

export function createPlace(placeName, placeType, placeAddress, placeNumber) {
    return fetch(`${baseUrl}/place`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: placeName, type: placeType, address: placeAddress, phone_number: placeNumber })
        })
        .then(response => response.json());
} 
