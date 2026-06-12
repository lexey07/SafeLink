import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import logo from "../assets/logo.png";

function Navbar() {

    const [user, setUser] = useState(null);
    useEffect(() => {
        loadUser();
    }, []);

    const loadUser = async () => {
        const token =
            localStorage.getItem("token");

        if (!token) return;

        try {
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
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div
            style={{
                width: "100%",
                height: "80px",
                background: "#0B254F",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "0 40px",
                boxSizing: "border-box",
                borderBottom: "1px solid #22365f",
            }}
        >
            <Link
                to="/dashboard"
                style={{
                    textDecoration: "none",
                }}
            >
                <div
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "15px",
                        filter: "drop-shadow(0 0 12px rgba(145,205,233,0.5))",
                    }}
                >
                    <img
                        src={logo}
                        alt="SafeLink"
                        style={{
                            width: "60px",
                            height: "60px",
                            objectFit: "contain",
                        }}
                    />

                    <div
                        style={{
                            color: "#FFFFFF",
                            fontSize: "28px",
                            fontWeight: "bold",
                            textShadow:
                                "0 0 15px rgba(125,211,252,0.45)",
                        }}
                    >
                        SafeLink
                    </div>
                </div>
            </Link>

            <div
                style={{
                    display: "flex",
                    gap: "30px",
                    alignItems: "center",
                }}
            >
                <Link
                    to="/dashboard"
                    style={{
                        color: "white",
                        textDecoration: "none",
                    }}
                >
                    Проверка
                </Link>

                <Link
                    to="/history"
                    style={{
                        color: "white",
                        textDecoration: "none",
                    }}
                >
                    История
                </Link>

                <Link
                    to="/learn"
                    style={{
                        color: "white",
                        textDecoration: "none",
                    }}
                >
                    Обучение
                </Link>

                <Link
                    to="/quiz"
                    style={{
                        color: "white",
                        textDecoration: "none",
                    }}
                >
                    Тест
                </Link>

                <Link
                    to="/ai"
                    style={{
                        color: "white",
                        textDecoration: "none",
                    }}
                >
                    Спросить ИИ
                </Link>

                <button
                    style={{
                        background: "#ffb800",
                        color: "#000",
                        border: "none",
                        padding: "10px 20px",
                        borderRadius: "10px",
                        fontWeight: "bold",
                        cursor: "pointer",
                    }}
                >
                    👑 Premium
                </button>

                <Link
                    to="/profile"
                    style={{
                        color: "white",
                        textDecoration: "none",
                        display: "flex",
                        alignItems: "center",
                        gap: "10px",
                        fontWeight: "bold",
                    }}
                >
                    <img
                        src={
                            user?.avatar ||
                            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                        }
                        alt=""
                        style={{
                            width: "40px",
                            height: "40px",
                            borderRadius: "50%",
                            objectFit: "cover",
                            border:
                                "2px solid #38BDF8",
                        }}
                    />

                    {user?.nickname ||
                        "Профиль"}
                </Link>
            </div>
        </div>
    );
}

export default Navbar;