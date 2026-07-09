import "./UrlInput.css";
import Button from "../UI/Button";

function UrlInput({
    url,
    setUrl,
    checkUrl,
}) {
    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            checkUrl();
        }
    };

    return (
        <div className="url-input-container">
            <input
                type="text"
                placeholder="Вставьте ссылку для проверки..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyDown={handleKeyDown}
                className="url-input"
            />

            <Button
                onClick={checkUrl}
            >
                🔍 Проверить ссылку
            </Button>
        </div>
    );
}

export default UrlInput;