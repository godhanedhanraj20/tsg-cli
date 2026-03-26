import { deleteFile, downloadFile } from '../api';

export default function FileTable({ folders, files, currentPath, setPath, refresh }) {

    const handleFolderClick = (folder) => {
        let newPath = currentPath;
        if (!newPath.endsWith('/')) newPath += '/';
        newPath += folder;
        if (!newPath.endsWith('/')) newPath += '/';
        setPath(newPath);
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure you want to delete this file?")) return;
        try {
            await deleteFile(id);
            refresh();
        } catch (error) {
            console.error('Delete failed:', error);
            alert('Delete failed');
        }
    };

    const handleDownload = (id) => {
        try {
            downloadFile(id);
        } catch (error) {
            console.error('Download failed:', error);
            alert('Download failed');
        }
    };

    return (
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
            <thead>
                <tr style={{ borderBottom: '2px solid #ddd', textAlign: 'left' }}>
                    <th style={{ padding: '10px' }}>Name</th>
                    <th style={{ padding: '10px' }}>Size</th>
                    <th style={{ padding: '10px' }}>Actions</th>
                </tr>
            </thead>
            <tbody>
                {folders.map((folder, index) => (
                    <tr key={`folder-${index}`} style={{ borderBottom: '1px solid #eee' }}>
                        <td style={{ padding: '10px' }}>
                            <span
                                onClick={() => handleFolderClick(folder)}
                                style={{ cursor: 'pointer', color: 'blue', textDecoration: 'underline' }}
                            >
                                📁 {folder}
                            </span>
                        </td>
                        <td style={{ padding: '10px' }}>-</td>
                        <td style={{ padding: '10px' }}>-</td>
                    </tr>
                ))}
                {files.map((file) => (
                    <tr key={`file-${file.id}`} style={{ borderBottom: '1px solid #eee' }}>
                        <td style={{ padding: '10px' }}>📄 {file.name}</td>
                        <td style={{ padding: '10px' }}>{file.size}</td>
                        <td style={{ padding: '10px' }}>
                            <button
                                onClick={() => handleDownload(file.id)}
                                style={{ marginRight: '10px', padding: '5px 10px', cursor: 'pointer' }}
                            >
                                Download
                            </button>
                            <button
                                onClick={() => handleDelete(file.id)}
                                style={{ padding: '5px 10px', cursor: 'pointer', color: 'white', backgroundColor: '#e74c3c', border: 'none', borderRadius: '3px' }}
                            >
                                Delete
                            </button>
                        </td>
                    </tr>
                ))}
                {folders.length === 0 && files.length === 0 && (
                    <tr>
                        <td colSpan="3" style={{ textAlign: 'center', padding: '20px', color: '#888' }}>
                            This folder is empty.
                        </td>
                    </tr>
                )}
            </tbody>
        </table>
    );
}
