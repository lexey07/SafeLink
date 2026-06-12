import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";

function Profile() {
    const [user, setUser] =
        useState(null);

    const [avatar, setAvatar] =
    useState("");

    useEffect(() => {
        loadProfile();
    }, []);

    const loadProfile =
        async () => {
            const token =
                localStorage.getItem(
                    "token"
                );

            const response =
                await fetch(
                    "http://127.0.0.1:8000/me",
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`,
                        },
                    }
                );

            const data =
                await response.json();

            setUser(data);
            setAvatar(data.avatar || "");
        };

        const saveAvatar = async () => {
            const token =
                localStorage.getItem("token");

            const response = await fetch(
                "http://127.0.0.1:8000/update-avatar",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json",
                        Authorization:
                            `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        avatar,
                    }),
                }
            );

            const data =
                await response.json();

            alert(data.message);

            loadProfile();
        };

    return (
        <>
            <Navbar />

            <div
                style={{
                    minHeight:
                        "100vh",
                    background:
                        "#061A40",
                    color: "white",
                    padding:
                        "40px",
                }}
            >
                <div
                    style={{
                        maxWidth:
                            "900px",
                        margin:
                            "0 auto",
                    }}
                >
                    <h1
                        style={{
                            textAlign:
                                "center",
                            marginBottom:
                                "40px",
                        }}
                    >
                        Профиль
                    </h1>

                    {user && (
                        <div
                            style={{
                                background: "rgba(16,45,94,0.65)",
                                borderRadius: "30px",
                                padding: "50px",
                                textAlign: "center",
                                border: "1px solid rgba(56,189,248,0.25)",
                                backdropFilter: "blur(10px)",
                                boxShadow:
                                    "0 0 35px rgba(56,189,248,0.08)",
                            }}
                        >
                            <img
                                src={
                                    user.avatar ||
                                    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                                }
                                alt=""
                                style={{
                                    width: "140px",
                                    height: "140px",
                                    borderRadius: "50%",
                                    objectFit: "cover",
                                    border: "3px solid #38BDF8",
                                    boxShadow:
                                        "0 0 30px rgba(56,189,248,0.55)",
                                    
                                }}
                            />

                            <h2>
                                {
                                    user.nickname
                                }
                            </h2>

                            <p>
                                {
                                    user.email
                                }
                            </p>

                            <div
                                style={{
                                    marginTop: "25px",
                                }}
                            >
                                <input
                                    type="text"
                                    placeholder="Ссылка на аватар"
                                    value={avatar}
                                    onChange={(e) =>
                                        setAvatar(
                                            e.target.value
                                        )
                                    }
                                    style={{
                                        width: "500px",
                                        padding: "12px",
                                        borderRadius: "12px",
                                        border:
                                            "1px solid #38BDF8",
                                        background:
                                            "radial-gradient(circle at top, rgba(56,189,248,0.12), #061A40 40%)",
                                        color: "white",
                                        boxSizing:
                                            "border-box",
                                        display: "block",
                                        margin: "0 auto",
                                    }}
                                />
                                <button
                                    onClick={saveAvatar}
                                    style={{
                                        width: "260px",
                                        padding: "16px",
                                        borderRadius: "18px",
                                        border: "none",
                                        background:
                                            "linear-gradient(90deg,#38BDF8,#3B82F6)",
                                        color: "white",
                                        fontWeight: "bold",
                                        fontSize: "18px",
                                        cursor: "pointer",
                                        display: "block",
                                        margin: "20px auto 0 auto",
                                        boxShadow:
                                            "0 0 20px rgba(56,189,248,0.35)",
                                    }}
                                >
                                    💾 Сохранить аватар
                                </button>

                                <button
                                    onClick={() => {
                                        localStorage.removeItem(
                                            "token"
                                        );

                                        window.location.href = "/";
                                    }}
                                    style={{
                                        width: "260px",
                                        padding: "16px",
                                        borderRadius: "18px",
                                        border:
                                            "1px solid rgba(56,189,248,0.35)",
                                        background: "transparent",
                                        color: "white",
                                        fontWeight: "bold",
                                        fontSize: "18px",
                                        cursor: "pointer",
                                        display: "block",
                                        margin: "15px auto 0 auto",
                                    }}
                                >
                                    ↩ Выйти
                                </button>
                            </div>

                            <div
                                style={{
                                    display: "flex",
                                    justifyContent: "center",
                                    gap: "40px",
                                    marginTop: "30px",
                                    marginBottom: "30px",
                                }}
                            >
                                <div
                                    style={{
                                        background: "rgba(6,26,64,0.8)",
                                        border:
                                            "1px solid rgba(56,189,248,0.15)",
                                        boxShadow:
                                            "0 0 20px rgba(56,189,248,0.08)",
                                    }}
                                >
                                    <div
                                        style={{
                                            fontSize: "42px",
                                            marginBottom: "10px",
                                        }}
                                    >
                                        🐟
                                    </div>

                                    <h3
                                        style={{
                                            margin: 0,
                                            color: "#BDEBFF",
                                        }}
                                    >
                                        Fish
                                    </h3>
                                    <p
                                        style={{
                                            fontSize: "42px",
                                            color: "#38BDF8",
                                            fontWeight: "bold",
                                        }}
                                    >
                                        {user.checks_left}
                                    </p>
                                </div>

                                <div
                                    style={{
                                        background: "rgba(6,26,64,0.8)",
                                        border:
                                            "1px solid rgba(56,189,248,0.15)",
                                        boxShadow:
                                            "0 0 20px rgba(56,189,248,0.08)",
                                    }}
                                >
                                    <div
                                        style={{
                                            fontSize: "42px",
                                            marginBottom: "10px",
                                        }}
                                    >
                                        👑
                                    </div>

                                    <h3
                                        style={{
                                            margin: 0,
                                            color: "#BDEBFF",
                                        }}
                                    >
                                        Premium
                                    </h3>
                                    <p
                                        style={{
                                            fontSize: "28px",
                                            color: user.is_premium
                                                ? "#38BDF8"
                                                : "#D6EAF8",
                                            fontWeight: "bold",
                                        }}
                                    >
                                        {user.is_premium
                                            ? "Активен"
                                            : "Не активен"}
                                    </p>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </>
    );
}

export default Profile;