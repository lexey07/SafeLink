import "./Toast.css";

function Toast({
    show,
    type,
    title,
    message,
}) {
    const icons = {
        success: "✅",
        error: "❌",
        info: "ℹ️",
        warning: "⚠️",
    };

    return (
        <div
            className={`toast ${show ? "show" : ""} ${type}`}
        >
            <div className="toast-header">

                <div className="toast-left">

                    <span className="toast-icon">
                        {icons[type]}
                    </span>

                    <span className="toast-title">
                        {title}
                    </span>

                </div>

                <button
                    className="toast-close"
                    onClick={() => {}}
                >
                    ✕
                </button>

            </div>

            <div className="toast-message">
                {message}
            </div>

            <div className="toast-progress" />
        </div>
    );
}

export default Toast;