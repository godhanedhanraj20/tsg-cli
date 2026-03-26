const API_URL = "http://127.0.0.1:8000";

const HEADERS = {
    "X-API-Key": "dev-secret-key"
};

export async function getFolder(path = "/") {
    const res = await fetch(`${API_URL}/folders?path=${encodeURIComponent(path)}`, {
        headers: HEADERS
    });
    return res.json();
}

export async function uploadFile(file, path = "/") {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_URL}/files/upload?path=${encodeURIComponent(path)}`, {
        method: "POST",
        headers: {
            "X-API-Key": "dev-secret-key"
        },
        body: formData
    });

    return res.json();
}

export async function deleteFile(id) {
    const res = await fetch(`${API_URL}/files/${id}`, {
        method: "DELETE",
        headers: HEADERS
    });
    return res.json();
}

export function downloadFile(id) {
    window.open(`${API_URL}/files/download/${id}`, "_blank");
}
