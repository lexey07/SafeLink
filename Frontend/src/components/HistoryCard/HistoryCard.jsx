import "./HistoryCard.css";

function HistoryCard({ item, expandedId, setExpandedId }) {
    const getStatusIcon = (status) => {
        switch (status) {
            case "Безопасно":
                return "🟢";
            case "Подозрительно":
                return "🟡";
            case "Высокий риск":
                return "🟠";
            case "Опасно":
                return "🔴";
            default:
                return "⚪";
        }
    };
    
    const getStatusClass = (status) => {
        switch (status) {
            case "Безопасно":
                return "safe";

            case "Подозрительно":
                return "warning";

            case "Высокий риск":
                return "high";

            case "Опасно":
                return "danger";

            default:
                return "";
        }
    };

    return (
        <div
            className={
                expandedId === item.id
                    ? "history-card expanded"
                    : "history-card"
            }
        >
            <div className="history-card-url">

                <p className="history-card-label">
                    🌐 Проверенная ссылка
                </p>

                <h2 className="history-card-domain">
                    {item.url}
                </h2>

                <p className="history-card-full-url">
                    {item.url}
                </p>

            </div>

            <div
                className={`status-badge ${getStatusClass(item.status)}`}
            >
                {getStatusIcon(item.status)}
                <span>{item.status}</span>
            </div>

            <p className="history-card-risk">
                Риск: {item.risk_score}/100
            </p>

            <button
                className="history-card-button"
                onClick={() =>
                    setExpandedId(
                        expandedId === item.id ? null : item.id
                    )
                }
            >
                {expandedId === item.id
                    ? "▲ Скрыть"
                    : "▼ Подробнее"}
            </button>

            {expandedId === item.id && (
                <div className="history-card-details">
                    <div>
                        <h3 className="history-title">
                            Причины анализа
                        </h3>

                        {item.reasons.map((reason, index) => (
                            <div
                                key={index}
                                className="reason-card"
                            >
                                • {reason}
                            </div>
                        ))}
                    </div>

                    <h3 className="ai-title">
                        🤖 Объяснение ИИ
                    </h3>

                    <div className="ai-box">
                        {item.ai_explanation}
                    </div>

                    <div className="history-date">
                        <span>📅 Проверено</span>

                        <span>
                            {new Date(
                                item.created_at
                            ).toLocaleString("ru-RU")}
                        </span>
                    </div>
                </div>
            )}
        </div>
    );
}

export default HistoryCard;