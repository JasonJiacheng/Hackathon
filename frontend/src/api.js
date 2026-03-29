const BASE_URL = "http://localhost:5000";

export async function apiPost(endpoint, body) {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
        method: "POST",
        body: body,
    });
    return response.json();
}

export async function apiGet(endpoint) {
    const response = await fetch(`${BASE_URL}${endpoint}`);
    return response.json();
}