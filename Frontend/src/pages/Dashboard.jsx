import React, { useEffect, useState } from "react";
import TopNavigation from "../components/TopNavigation";
import PageHeader from "../components/PageHeader";
import PageContainer from "../components/PageContainer";
import DashboardStats from "../components/DashboardStats/DashboardStats";
import UrlInput from "../components/UrlInput/UrlInput";
import ResultCard from "../components/ResultCard/ResultCard";
import ErrorMessage from "../components/ErrorMessage/ErrorMessage";
import { checkUrl } from "../services/urlService";
import { getRecommendation } from "../services/recommendationService";
import "./Dashboard.css";

function Dashboard() {
    const [url, setUrl] = useState("");
    const [result, setResult] = useState(null);
    const [userInfo, setUserInfo] = useState(null);

    useEffect(() => {
        loadUserInfo();
    }, []);

    const loadUserInfo = async () => {
        try {
            const token = localStorage.getItem("token");

            const response = await fetch(
                "http://127.0.0.1:8000/me",
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            const data = await response.json();

            setUserInfo(data);
        } catch (error) {
            console.error(error);
        }
    };

  const handleSubmit = async () => {

    if (url.trim() === "") {
      setResult({
        message: "Введите ссылку для проверки",
      });
      return;
    }

    if (url.trim().length < 4) {
      setResult({
        message: "Ссылка слишком короткая",
      });
      return;
    }

    try {
      const token = localStorage.getItem("token");
      const data = await checkUrl(url, token);
      if (data.risk_score !== undefined) {
        const recommendation = getRecommendation(data.risk_score);
        setResult({
            ...data,
            recommendation,
        });

        setUserInfo((prev) => ({
            ...prev,
            checks_left: data.checks_left ?? prev?.checks_left,
            is_premium: data.is_premium ?? prev?.is_premium,
        }));
      } else {
        setResult(data);
      }
    } catch (error) {
      setResult({
        message: "Ошибка подключения к серверу",
      });
    }
  };

  const showErrorMessage =
    result && result.message && !result.url;

  const showResultCard =
    result && result.url;

  return (
    <div className="dashboard">
      <TopNavigation />
      <PageContainer>
        <PageHeader
            title="SafeLink"
            subtitle="Проверяйте ссылки на фишинг быстро и безопасно"
        />
        <DashboardStats
            result={
                result
                    ? {
                        ...userInfo,
                        ...result,
                    }
                    : userInfo
            }
        />
        <UrlInput
        url={url}
        setUrl={setUrl}
        checkUrl={handleSubmit}
        />
        {showErrorMessage && (
          <ErrorMessage message={result.message} />
        )}
        {showResultCard && (
          <ResultCard result={result} />
        )}
      </PageContainer>
    </div>
  );
}

export default Dashboard;