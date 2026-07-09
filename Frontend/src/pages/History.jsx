import { useEffect, useMemo, useState } from "react";

import HistoryCard from "../components/HistoryCard";
import HistoryStats from "../components/HistoryStats";
import SearchBar from "../components/SearchBar";
import FilterBar from "../components/FilterBar";
import Loader from "../components/Loader";
import EmptyHistory from "../components/EmptyHistory";
import TopNavigation from "../components/TopNavigation";
import PageHeader from "../components/PageHeader";
import PageContainer from "../components/PageContainer";
import "./History.css";

function History() {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [expandedId, setExpandedId] = useState(null);

    const [search, setSearch] = useState("");
    const [filter, setFilter] = useState("all");

    useEffect(() => {
        const loadHistory = async () => {
            try {
                const token = localStorage.getItem("token");

                const response = await fetch(
                    "http://127.0.0.1:8000/history",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );

                const data = await response.json();
                setHistory(data);
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        loadHistory();
    }, []);

    const filteredHistory = useMemo(() => {
        return history.filter((item) => {
            const matchesSearch = item.url
                .toLowerCase()
                .includes(search.toLowerCase());

            let matchesFilter = true;

            switch (filter) {
                case "safe":
                    matchesFilter = item.status === "Безопасно";
                    break;

                case "suspicious":
                    matchesFilter =
                        item.status === "Подозрительно";
                    break;

                case "danger":
                    matchesFilter =
                        item.status === "Опасно" ||
                        item.status === "Высокий риск";
                    break;

                default:
                    matchesFilter = true;
            }

            return matchesSearch && matchesFilter;
        });
    }, [history, search, filter]);

    if (loading) {
            return <Loader />;
        }

        const sortedHistory = [...filteredHistory].sort((a, b) => {

        if (a.id === expandedId) return -1;

        if (b.id === expandedId) return 1;

        return 0;

    });

    return (
        <div className="history-page">
          <TopNavigation />

          <PageContainer>

          <PageHeader
                title="История проверок"
                subtitle="Все ранее проверенные ссылки"
            />

            {history.length > 0 && (
                <>
                    <HistoryStats history={history} />

                    <SearchBar
                        search={search}
                        setSearch={setSearch}
                    />

                    <FilterBar
                        filter={filter}
                        setFilter={setFilter}
                    />
                </>
            )}

            {history.length === 0 ? (
                <EmptyHistory />
            ) : filteredHistory.length === 0 ? (
                <EmptyHistory
                    title="Ничего не найдено"
                    subtitle="Попробуйте изменить поисковый запрос или фильтр."
                />
            ) : (
                <div className="history-grid">
                    {sortedHistory.map((item) => (
                        <HistoryCard
                            key={item.id}
                            item={item}
                            expandedId={expandedId}
                            setExpandedId={setExpandedId}
                        />
                    ))}
                </div>
            )}
          </PageContainer>
        </div>
    );
}

export default History;