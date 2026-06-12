import { useState } from "react";
import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();

        const response = await fetch(
            "http://127.0.0.1:8000/login",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email,
                    password,
                }),
            }
        );

        const data = await response.json();

        if (data.token) {
            localStorage.setItem("token", data.token);

            window.location.href =
                "/dashboard";
        } else {
            alert(
                data.message || "Ошибка входа"
            );
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
                    width: "450px",
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
                                "0 0 35px rgba(125,211,252,0.7)"
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
                        Вход в аккаунт
                    </p>
                </div>

                <form onSubmit={handleLogin}>
                    <label>
                        Email адрес
                    </label>

                    <input
                        type="email"
                        autoComplete="email"
                        placeholder="Введите почту"
                        value={email}
                        onChange={(e) =>
                            setEmail(e.target.value)
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

                    <label>
                        Пароль
                    </label>

                    <input
                        type="password"
                        autoComplete="current-password"
                        placeholder="Введите пароль"
                        value={password}
                        onChange={(e) =>
                            setPassword(
                                e.target.value
                            )
                        }
                        style={{
                            width: "100%",
                            padding: "14px",
                            marginTop: "8px",
                            marginBottom: "25px",
                            borderRadius: "12px",
                            border:
                                "1px solid #38BDF8",
                            background: "#061A40",
                            color: "white",
                            boxSizing: "border-box",
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
                        Войти
                    </button>
                </form>

                <p
                    style={{
                        textAlign: "center",
                        marginTop: "25px",
                    }}
                >
                    Нет аккаунта?{" "}
                    <Link
                        to="/register"
                        style={{
                            color: "#7DD3FC",
                        }}
                    >
                        Зарегистрироваться
                    </Link>
                </p>
            </div>
        </div>
    );
}

export default Login;