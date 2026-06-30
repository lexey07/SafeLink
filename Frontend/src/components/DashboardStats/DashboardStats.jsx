import "./DashboardStats.css";
import Card from "../UI/Card";

function DashboardStats({ result }) {
    const stats = [
        {
            icon: "🐟",
            title: "Осталось Fish",
            value: result?.checks_left ?? "-",
        },
        {
            icon: "👑",
            title: "Premium",
            value: result?.is_premium ? "Активен" : "Не активен",
        },
        {
            icon: "🛡️",
            title: "Результат проверки",
            value: result?.status ?? "-",
        },
    ];

    return (
        <div className="dashboard-stats">
            {stats.map((item) => (
                <Card
                    key={item.title}
                    className="dashboard-stat-card"
                >
                    <div className="dashboard-stat-icon">
                        {item.icon}
                    </div>

                    <div className="dashboard-stat-title">
                        {item.title}
                    </div>

                    <div className="dashboard-stat-value">
                        {item.value}
                    </div>
                </Card>
            ))}
        </div>
    );
}

export default DashboardStats;