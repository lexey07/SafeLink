import Navbar from "../components/Navbar";
import { useState } from "react";

function Dashboard() {
    const [url, setUrl] = useState("");
    const [result, setResult] = useState(null);

    const checkUrl = async () => {
        if (!url.trim()) {
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

            const response = await fetch(
                "http://127.0.0.1:8000/check-url",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        url: url,
                    }),
                }
            );

            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error(error);

            setResult({
                message: "Ошибка подключения к серверу",
            });
        }
    };

    let recommendationTitle = "🛡️ Рекомендация SafeLink";
    let recommendationText = "";

    if (result?.risk_score === 0) {
        recommendationText =
            "Сайт выглядит безопасным. Тем не менее всегда проверяйте адрес сайта перед вводом паролей и банковских данных.";
    }
    else if (result?.risk_score <= 35) {
        recommendationText =
            "Обнаружены незначительные признаки риска. Рекомендуется внимательно проверить адрес сайта перед вводом личных данных.";
    }
    else if (result?.risk_score <= 65) {
        recommendationText =
            "Обнаружено несколько подозрительных признаков. Не рекомендуется вводить пароли, коды подтверждения или банковские данные без дополнительной проверки.";
    }
    else {
        recommendationText =
            "Высока вероятность мошенничества или фишинга. Не вводите личные данные и не переходите по ссылке без необходимости.";
    }

    return (
        <>
            <Navbar />

            <div
                style={{
                    minHeight: "100vh",
                    background: "#061A40",
                    color: "#FFFFFF",
                    padding: "40px",
                    fontFamily: "Arial, sans-serif",
                }}
            >
                <div
                    style={{
                        maxWidth: "1100px",
                        margin: "0 auto",
                    }}
                >
                    <h1
                        style={{
                            textAlign: "center",
                            fontSize: "72px",
                            fontWeight: "800",
                            marginBottom: "50px",
                            color: "#FFFFFF",
                            textShadow:
                                "0 0 25px rgba(152, 214, 243, 0.6)",
                        }}
                    >
                        SafeLink
                    </h1>

                    <p
                        style={{
                            textAlign: "center",
                            color: "#D6EAF8",
                            marginBottom: "50px",
                            fontSize: "24px",
                        }}
                    >
                        Проверка ссылок на фишинг и мошенничество
                    </p>

                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            gap: "25px",
                            marginBottom: "50px",
                            flexWrap: "wrap",
                        }}
                    >
                        <div
                            style={{
                                background: "#102D5E",
                                border:
                                    "1px solid rgba(125,211,252,0.25)",
                                boxShadow:
                                    "0 0 20px rgba(56,189,248,0.12)",
                                padding: "25px",
                                borderRadius: "20px",
                                minWidth: "220px",
                                textAlign: "center",
                            }}
                        >
                            <h3>🐟 Fish</h3>

                            <p
                                style={{
                                    fontSize: "32px",
                                    color: "#7DD3FC",
                                    fontWeight: "bold",
                                }}
                            >
                                {result?.checks_left ?? "-"}
                            </p>
                        </div>

                        <div
                            style={{
                                background: "#102D5E",
                                border:
                                    "1px solid rgba(125,211,252,0.25)",
                                boxShadow:
                                    "0 0 20px rgba(56,189,248,0.12)",
                                padding: "25px",
                                borderRadius: "20px",
                                minWidth: "220px",
                                textAlign: "center",
                            }}
                        >
                            <h3>👑 Premium</h3>

                            <p
                                style={{
                                    fontSize: "22px",
                                }}
                            >
                                {result?.premium
                                    ? "Активен"
                                    : "Не активен"}
                            </p>
                        </div>

                        <div
                            style={{
                                background: "#102D5E",
                                border:
                                    "1px solid rgba(125,211,252,0.25)",
                                boxShadow:
                                    "0 0 20px rgba(56,189,248,0.12)",
                                padding: "25px",
                                borderRadius: "20px",
                                minWidth: "220px",
                                textAlign: "center",
                            }}
                        >
                            <h3>🛡️ Статус</h3>

                            <p
                                style={{
                                    fontSize: "22px",
                                }}
                            >
                                {result?.status || "-"}
                            </p>
                        </div>
                    </div>

                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            gap: "15px",
                            marginBottom: "40px",
                        }}
                    >
                        <input
                            type="text"
                            placeholder="Вставьте ссылку..."
                            value={url}
                            onChange={(e) =>
                                setUrl(e.target.value)
                            }
                            style={{
                                width: "650px",
                                padding: "18px",
                                borderRadius: "16px",
                                border: "1px solid #38BDF8",
                                background: "#102D5E",
                                color: "white",
                                fontSize: "16px",
                                outline: "none",
                            }}
                        />

                        <button
                            onClick={checkUrl}
                            style={{
                                padding: "18px 28px",
                                borderRadius: "16px",
                                border: "none",
                                cursor: "pointer",
                                fontWeight: "bold",
                                background: "#38BDF8",
                                color: "white",
                            }}
                        >
                            Проверить
                        </button>
                    </div>

                    {result && result.message && (
                        <div
                            style={{
                                marginTop: "30px",
                                background: "#102D5E",
                                padding: "25px",
                                borderRadius: "20px",
                                maxWidth: "800px",
                                marginInline: "auto",
                            }}
                        >
                            <h3>{result.message}</h3>
                        </div>
                    )}

                    {result && result.status && (
                        <div
                            style={{
                                marginTop: "40px",
                                maxWidth: "800px",
                                marginInline: "auto",
                                background: "#102D5E",
                                border:
                                    "1px solid rgba(125,211,252,0.25)",
                                boxShadow:
                                    "0 0 30px rgba(56,189,248,0.15)",
                                borderRadius: "24px",
                                padding: "35px",
                            }}
                        >
                            <h2>
                                {result.status === "Безопасно" &&
                                    "🟢 Безопасная ссылка"}

                                {result.status === "Подозрительно" &&
                                    "🟡 Подозрительная ссылка"}

                                {result.status === "Высокий риск" &&
                                    "🟠 Высокий риск фишинга"}

                                {result.status === "Опасно" &&
                                    "🔴 Опасная ссылка"}
                            </h2>

                            <p>
                                <strong>URL:</strong>{" "}
                                {result.url}
                            </p>

                            <p>
                                <strong>Риск:</strong>{" "}
                                {result.risk_score}/100
                            </p>

                            <div
                                style={{
                                    width: "100%",
                                    height: "18px",
                                    background: "#061A40",
                                    borderRadius: "999px",
                                    overflow: "hidden",
                                    marginTop: "15px",
                                    marginBottom: "25px",
                                }}
                            >
                                <div
                                    style={{
                                        width: `${result.risk_score}%`,
                                        height: "100%",
                                        background:
                                            result.risk_score >=
                                            60
                                                ? "#ef4444"
                                                : result.risk_score >=
                                                  30
                                                ? "#f59e0b"
                                                : "#22c55e",
                                        transition: "0.4s",
                                    }}
                                />
                            </div>

                            <h3>Причины анализа</h3>

                            {result.reasons &&
                            result.reasons.length > 0 ? (
                                <>
                                    <ul
                                        style={{
                                            textAlign: "left",
                                            marginTop: "15px",
                                            fontSize: "14px",
                                            lineHeight: "1.5",
                                        }}
                                    >
                                        {result.reasons.slice(0, 5).map(
                                            (
                                                reason,
                                                index
                                            ) => (
                                                <li key={index}>
                                                    {reason}
                                                </li>
                                            )
                                        )}
                                    </ul>
                                    
                                    <div
                                        style={{
                                            marginTop: "25px",
                                            background: "#102D5E",
                                            border: "1px solid rgba(56,189,248,0.35)",
                                            borderRadius: "18px",
                                            padding: "22px",
                                            color: "#D6E8FF",
                                            boxShadow:
                                                "0 0 25px rgba(56,189,248,0.08)",
                                        }}
                                    >
                                        <h3
                                            style={{
                                                marginTop: 0,
                                                marginBottom: "12px",
                                                color: "#38BDF8",
                                            }}
                                        >
                                            🛡️ Рекомендация SafeLink
                                        </h3>

                                        <p
                                        style={{
                                            margin: 0,
                                            lineHeight: "1.8",
                                            fontSize: "15px",
                                        }}
                                    >
                                        {recommendationText}
                                    </p>
                                    </div>
                                </>
                            ) : (
                                <p
                                    style={{
                                        color: "#7DD3FC",
                                        marginTop: "15px",
                                    }}
                                >
                                    ✅ Подозрительных признаков не обнаружено
                                </p>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </>
    );
}

export default Dashboard;