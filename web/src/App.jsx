import { useState, useEffect, useCallback } from 'react';
import { getFolder } from './api';
import Breadcrumb from './components/Breadcrumb';
import UploadBox from './components/UploadBox';
import FileTable from './components/FileTable';

function App() {
    const [currentPath, setCurrentPath] = useState('/');
    const [folders, setFolders] = useState([]);
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(true);

    const loadData = useCallback(async () => {
        setLoading(true);
        try {
            const data = await getFolder(currentPath);
            if (data.status === 'success') {
                setFolders(data.data.folders || []);
                setFiles(data.data.files || []);
            } else {
                console.error("Error from API:", data.message);
                setFolders([]);
                setFiles([]);
            }
        } catch (error) {
            console.error("Failed to load folder:", error);
            setFolders([]);
            setFiles([]);
        } finally {
            setLoading(false);
        }
    }, [currentPath]);

    useEffect(() => {
        loadData();
    }, [loadData]);

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto', fontFamily: 'Arial, sans-serif' }}>
            <h1>TSG-CLI Web Browser</h1>

            <Breadcrumb currentPath={currentPath} setPath={setCurrentPath} />

            <UploadBox currentPath={currentPath} refresh={loadData} />

            {loading ? (
                <p>Loading...</p>
            ) : (
                <FileTable
                    folders={folders}
                    files={files}
                    currentPath={currentPath}
                    setPath={setCurrentPath}
                    refresh={loadData}
                />
            )}
        </div>
    );
}

export default App;
