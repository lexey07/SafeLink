import "./Card.css";

function Card({
    children,
    className = "",
}) {
    return (
        <div
            className={`sl-card ${className}`}
        >
            {children}
        </div>
    );
}

export default Card;