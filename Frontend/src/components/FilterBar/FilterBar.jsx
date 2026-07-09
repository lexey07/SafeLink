import "./FilterBar.css";

function FilterBar({ filter, setFilter }) {
    const filters = [
        { key: "all", label: "📋 Все" },
        { key: "safe", label: "🟢 Безопасные" },
        { key: "suspicious", label: "🟡 Подозрительные" },
        { key: "danger", label: "🔴 Опасные" },
    ];

    return (
        <div className="filter-bar">
            {filters.map((item) => (
                <button
                    key={item.key}
                    className={
                        filter === item.key
                            ? "filter-button active"
                            : "filter-button"
                    }
                    onClick={() => setFilter(item.key)}
                >
                    {item.label}
                </button>
            ))}
        </div>
    );
}

export default FilterBar;