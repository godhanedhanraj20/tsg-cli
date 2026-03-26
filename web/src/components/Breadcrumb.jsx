export default function Breadcrumb({ currentPath, setPath }) {
    const parts = currentPath.split('/').filter(Boolean);

    const handleClick = (index) => {
        if (index === -1) {
            setPath('/');
            return;
        }
        const newPath = '/' + parts.slice(0, index + 1).join('/') + '/';
        setPath(newPath);
    };

    return (
        <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>
            <span
                onClick={() => handleClick(-1)}
                style={{ cursor: 'pointer', color: 'blue', textDecoration: 'underline' }}
            >
                Root
            </span>
            {parts.map((part, index) => (
                <span key={index}>
                    {' / '}
                    <span
                        onClick={() => handleClick(index)}
                        style={{ cursor: 'pointer', color: 'blue', textDecoration: 'underline' }}
                    >
                        {part}
                    </span>
                </span>
            ))}
        </div>
    );
}
