import "./ResultCard.css";

function ResultCard({ result }) {
    if (!result || !result.status) {
        return null;
    }

    const getStatusTitle = () => {
        switch (result.status) {
            case "Безопасно":
                return "🟢 Безопасная ссылка";

            case "Подозрительно":
                return "🟡 Подозрительная ссылка";

            case "Высокий риск":
                return "🟠 Высокий риск фишинга";

            case "Опасно":
                return "🔴 Опасная ссылка";

            default:
                return result.status;
        }
    };

    const getRiskColor = () => {
        if (result.risk_score >= 60) return "#EF4444";
        if (result.risk_score >= 30) return "#F59E0B";
        return "#22C55E";
    };

    return (
        <div className="result-card">
            <h2>{getStatusTitle()}</h2>

            <p>
                <strong>URL:</strong> {result.url}
            </p>

            <p>
                <strong>Риск:</strong> {result.risk_score}/100
            </p>

            <div className="risk-bar">
                <div
                    className="risk-progress"
                    style={{
                        width: `${result.risk_score}%`,
                        background: getRiskColor(),
                    }}
                />
            </div>

            <h3>Причины анализа</h3>

            {result.reasons.length > 0 ? (
                <>
                    <div className="reasons">
                        {result.reasons.slice(0, 5).map((reason, index) => (
                            <div
                                key={index}
                                className="reason-item"
                            >
                                • {reason}
                            </div>
                        ))}
                    </div>

                    {result.ai_explanation && (
                        <div className="ai-box">
                            <h3>🤖 Объяснение ИИ</h3>

                            <p>
                                {result.ai_explanation}
                            </p>
                        </div>
                    )}

                    <div className="recommendation-box">
                        <h3>🛡️ Рекомендация SafeLink</h3>

                        <p>{result.recommendation}</p>
                    </div>
                </>
            ) : (
                <p className="safe-text">
                    ✅ Подозрительных признаков не обнаружено
                </p>
            )}
        </div>
    );
}

export default ResultCard;