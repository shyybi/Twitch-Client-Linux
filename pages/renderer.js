const axios = require('axios');

const CLIENT_ID = "oi0rtnk972zackbs4dzimsiwycdh9f";
const CLIENT_SECRET = "pt5q7ao0xk56x0cxwxnvxnb3ax5kjo";

async function getOAuthToken() {
    const url = `https://id.twitch.tv/oauth2/token?client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&grant_type=client_credentials`;
    const response = await axios.post(url);
    return response.data.access_token;
}

async function getTopStreams(limit = 10) {
    const url = `https://api.twitch.tv/helix/streams?first=${limit}`;
    const oauthToken = await getOAuthToken();
    const headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': `Bearer ${oauthToken}`
    };
    
    try {
        const response = await axios.get(url, { headers });
        return response.data.data;
    } catch (error) {
        console.error("Erreur lors de la récupération des streams:", error);
        return null;
    }
}

function updateTable(streams) {
    const tableBody = document.getElementById('streamsBody');
    tableBody.innerHTML = '';

    streams.forEach(stream => {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = stream.user_name;
        row.insertCell(1).textContent = stream.game_name;
        row.insertCell(2).textContent = stream.viewer_count;
    });
}

async function refreshStreams() {
    const streams = await getTopStreams();
    if (streams) {
        updateTable(streams);
    } else {
        console.error("Impossible de récupérer les streams");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const refreshButton = document.getElementById('refreshButton');
    refreshButton.addEventListener('click', refreshStreams);

    refreshStreams();
});
