import { useState } from 'react';
import { uploadFile } from '../api';

export default function UploadBox({ currentPath, refresh }) {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);

    const handleUpload = async () => {
        if (!file) return;
        setUploading(true);
        try {
            await uploadFile(file, currentPath);
            setFile(null);
            document.getElementById('file-upload-input').value = '';
            refresh();
        } catch (error) {
            console.error('Upload failed:', error);
            alert('Upload failed');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '4px' }}>
            <h3>Upload File to {currentPath}</h3>
            <input
                id="file-upload-input"
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                disabled={uploading}
                style={{ marginRight: '10px' }}
            />
            <button onClick={handleUpload} disabled={!file || uploading}>
                {uploading ? 'Uploading...' : 'Upload'}
            </button>
        </div>
    );
}
