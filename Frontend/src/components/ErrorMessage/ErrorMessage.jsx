import "./ErrorMessage.css";

function ErrorMessage({ message }) {
    if (!message) {
        return null;
    }

    return (
        <div className="error-message">
            <h3>{message}</h3>
        </div>
    );
}

export default ErrorMessage;