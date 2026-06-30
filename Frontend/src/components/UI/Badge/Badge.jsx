import "./Badge.css";

function Badge({
    children,
    type = "info",
}) {
    return (
        <div
            className={`sl-badge ${type}`}
        >
            {children}
        </div>
    );
}

export default Badge;