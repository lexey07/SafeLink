import "./HistoryStats.css";

function HistoryStats({ history }) {
    const total = history.length;

    const safe = history.filter(
        (item) => item.status === "Безопасно"
    ).length;

    const suspicious = history.filter(
        (item) => item.status === "Подозрительно"
    ).length;

    const danger = history.filter(
        (item) =>
            item.status === "Опасно" ||
            item.status === "Высокий риск"
    ).length;

    const stats = [
        {
            title: "Всего проверок",
            value: total,
            icon: "📊",
        },
        {
            title: "Безопасные",
            value: safe,
            icon: "🟢",
        },
        {
            title: "Подозрительные",
            value: suspicious,
            icon: "🟡",
        },
        {
            title: "Опасные",
            value: danger,
            icon: "🔴",
        },
    ];

    return (
        <div className="history-stats">
            {stats.map((stat) => (
                <div
                    key={stat.title}
                    className="history-stat-card"
                >
                    <div className="history-stat-icon">
                        {stat.icon}
                    </div>

                    <div className="history-stat-title">
                        {stat.title}
                    </div>

                    <div className="history-stat-value">
                        {stat.value}
                    </div>
                </div>
            ))}
        </div>
    );
}

export default HistoryStats;