import "./EmptyHistory.css";

function EmptyHistory({
    title = "История пока пуста",
    subtitle = "Проверьте первую ссылку на главной странице."
}) {
    return (
        <div className="empty-history">
            <div className="empty-icon">
                🔍
            </div>

            <h2>{title}</h2>

            <p>{subtitle}</p>
        </div>
    );
}

export default EmptyHistory;