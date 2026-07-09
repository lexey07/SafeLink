import "./Button.css";

function Button({
    children,
    onClick,
    type = "primary",
    disabled = false,
}) {
    return (
        <button
            className={`sl-button ${type}`}
            onClick={onClick}
            disabled={disabled}
        >
            {children}
        </button>
    );
}

export default Button;