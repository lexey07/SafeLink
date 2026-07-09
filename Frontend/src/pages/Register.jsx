import { useState } from "react";
import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

function Register() {
    const [email, setEmail] = useState("");
    const [nickname, setNickname] = useState("");
    const [password, setPassword] = useState("");

    const handleRegister = async (e) => {
        e.preventDefault();

        const response = await fetch(
            "http://127.0.0.1:8000/register",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email,
                    nickname,
                    password,
                }),
            }
        );

        const data = await response.json();

        if (data.email) {
            localStorage.setItem(
                "verify_email",
                data.email
            );

            window.location.href =
                "/verify-email";
        }
    };

    return (
        <div
            style={{
                minHeight: "100vh",
                background: "#061A40",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                color: "white",
                fontFamily: "Arial",
            }}
        >
            <div
                style={{
                    background: "#102D5E",
                    padding: "50px",
                    borderRadius: "25px",
                    width: "500px",
                    border:
                        "1px solid rgba(125,211,252,0.25)",
                    boxShadow:
                        "0 0 30px rgba(56,189,248,0.15)",
                }}
            >
                <div
                    style={{
                        textAlign: "center",
                        marginBottom: "30px",
                    }}
                >
                    <img
                        src={logo}
                        alt="SafeLink"
                        style={{
                            width: "120px",
                            marginBottom: "25px",
                        }}
                    />

                    <h1
                        style={{
                            margin: 0,
                            fontSize: "42px",
                            color: "#FFFFFF",
                            textShadow:
                                "0 0 35px rgba(125,211,252,0.7)",
                        }}
                    >
                        SafeLink
                    </h1>

                    <p
                        style={{
                            color: "#D6EAF8",
                            marginTop: "10px",
                        }}
                    >
                        Создание аккаунта
                    </p>
                </div>

                <form onSubmit={handleRegister}>
                    <label>Email адрес</label>

                    <input
                        type="email"
                        placeholder="Введите почту"
                        value={email}
                        onChange={(e) =>
                            setEmail(e.target.value)
                        }
                        autoComplete="email"
                        style={{
                            width: "100%",
                            padding: "14px",
                            marginTop: "8px",
                            marginBottom: "20px",
                            borderRadius: "12px",
                            border:
                                "1px solid #38BDF8",
                            background: "#061A40",
                            color: "white",
                            boxSizing: "border-box",
                        }}
                    />

                    <label>Никнейм</label>

                    <input
                        type="text"
                        placeholder="Придумайте никнейм"
                        value={nickname}
                        onChange={(e) =>
                            setNickname(e.target.value)
                        }
                        style={{
                            width: "100%",
                            padding: "14px",
                            marginTop: "8px",
                            marginBottom: "20px",
                            borderRadius: "12px",
                            border:
                                "1px solid #38BDF8",
                            background: "#061A40",
                            color: "white",
                            boxSizing: "border-box",
                        }}
                    />

                    <label>Пароль</label>

                    <input
                        type="password"
                        placeholder="Введите пароль"
                        value={password}
                        onChange={(e) =>
                            setPassword(e.target.value)
                        }
                        autoComplete="new-password"
                        style={{
                            width: "100%",
                            padding: "14px",
                            marginTop: "8px",
                            marginBottom: "20px",
                            borderRadius: "12px",
                            border:
                                "1px solid #38BDF8",
                            background: "#061A40",
                            color: "white",
                            boxSizing: "border-box",
                        }}
                    />

                    <label>
                        Фото профиля
                        (необязательно)
                    </label>

                    <input
                        type="file"
                        style={{
                            width: "100%",
                            marginTop: "10px",
                            marginBottom: "25px",
                            color: "white",
                        }}
                    />

                    <button
                        type="submit"
                        style={{
                            width: "100%",
                            padding: "15px",
                            borderRadius: "12px",
                            border: "none",
                            background:
                                "#38BDF8",
                            color: "white",
                            fontWeight: "bold",
                            cursor: "pointer",
                            fontSize: "16px",
                        }}
                    >
                        Создать аккаунт
                    </button>
                </form>

                <p
                    style={{
                        textAlign: "center",
                        marginTop: "25px",
                    }}
                >
                    Уже есть аккаунт?{" "}
                    <Link
                        to="/"
                        style={{
                            color: "#7DD3FC",
                        }}
                    >
                        Войти
                    </Link>
                </p>
            </div>
        </div>
    );
}

export default Register;