import { useState, useEffect } from "react";

function VerifyEmail() {
    const [email] = useState(
        localStorage.getItem("verify_email") || ""
    );

    const [code, setCode] = useState([
        "",
        "",
        "",
        "",
        "",
        "",
    ]);

    const [timer, setTimer] = useState(60);

    const handleCodeChange = (
        value,
        index
    ) => {
        if (!/^\d?$/.test(value)) return;

        const newCode = [...code];

        newCode[index] = value;

        setCode(newCode);

        if (value && index < 5) {
            document
                .getElementById(
                    `code-${index + 1}`
                )
                ?.focus();
        }
    };

    const handleKeyDown = (
        e,
        index
    ) => {
        if (e.key === "Backspace") {

            const newCode = [...code];

            if (newCode[index] !== "") {

                for (
                    let i = index;
                    i < 5;
                    i++
                ) {
                    newCode[i] =
                        newCode[i + 1];
                }

                newCode[5] = "";

                setCode(newCode);

                e.preventDefault();

                return;
            }

            if (index > 0) {
                document
                    .getElementById(
                        `code-${index - 1}`
                    )
                    ?.focus();
            }
        }
    };

    const handlePaste = (e) => {
        const pasted = e.clipboardData
            .getData("text")
            .trim();

        if (!/^\d{6}$/.test(pasted))
            return;

        setCode(pasted.split(""));
    };

    const verify = async () => {
        const response = await fetch(
            "http://127.0.0.1:8000/verify-email",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json",
                },
                body: JSON.stringify({
                    email,
                    code: code.join(""),
                }),
            }
        );

        const resendCode = async () => {
            const response = await fetch(
                "http://127.0.0.1:8000/resend-code",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json",
                    },
                    body: JSON.stringify({
                        email,
                        code: "000000",
                    }),
                }
            );

            const data =
                await response.json();

            alert(data.message);

            setTimer(60);
        };

        const data = await response.json();

        if (data.token) {
            localStorage.setItem(
                "token",
                data.token
            );

            window.location.href =
                "/dashboard";
        } else {
            alert(data.message);
        }
    };

    useEffect(() => {
        if (timer <= 0) return;

        const interval = setInterval(() => {
            setTimer((prev) => prev - 1);
        }, 1000);

        return () => clearInterval(interval);
    }, [timer]);

    return (
        <div
            style={{
                minHeight: "100vh",
                background: "#061A40",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                color: "white",
                fontFamily:
                    "Arial, sans-serif",
            }}
        >
            <div
                style={{
                    width: "700px",
                    background: "#102D5E",
                    padding: "50px",
                    borderRadius: "25px",
                    textAlign: "center",
                    border:
                        "1px solid rgba(125,211,252,0.25)",
                    boxShadow:
                        "0 0 30px rgba(56,189,248,0.15)",
                }}
            >
                <h1
                    style={{
                        fontSize: "52px",
                        marginBottom: "20px",
                        color: "#FFFFFF",
                        textShadow:
                            "0 0 35px rgba(125,211,252,0.7)",
                    }}
                >
                    Подтверждение Email
                </h1>

                <p
                    style={{
                        color: "#D6EAF8",
                        fontSize: "20px",
                        marginBottom: "40px",
                    }}
                >
                    Введите 6-значный код
                    подтверждения
                </p>

                <div
                    style={{
                        display: "flex",
                        justifyContent:
                            "center",
                        gap: "12px",
                        marginBottom: "40px",
                    }}
                >
                    {code.map(
                        (
                            digit,
                            index
                        ) => (
                            <input
                                key={
                                    index
                                }
                                id={`code-${index}`}
                                type="text"
                                maxLength={1}
                                value={
                                    digit
                                }
                                onChange={(
                                    e
                                ) =>
                                    handleCodeChange(
                                        e
                                            .target
                                            .value,
                                        index
                                    )
                                }
                                onKeyDown={(
                                    e
                                ) =>
                                    handleKeyDown(
                                        e,
                                        index
                                    )
                                }
                                onPaste={
                                    index ===
                                    0
                                        ? handlePaste
                                        : undefined
                                }
                                style={{
                                    width:
                                        "70px",
                                    height:
                                        "80px",
                                    textAlign:
                                        "center",
                                    fontSize:
                                        "34px",
                                    borderRadius:
                                        "15px",
                                    border:
                                        "2px solid #38BDF8",
                                    background:
                                        "#061A40",
                                    color:
                                        "white",
                                    outline:
                                        "none",
                                    boxSizing:
                                        "border-box",
                                }}
                            />
                        )
                    )}
                </div>

                <button
                    onClick={verify}
                    style={{
                        width: "100%",
                        padding: "18px",
                        borderRadius:
                            "15px",
                        border: "none",
                        background:
                            "#38BDF8",
                        color: "white",
                        fontWeight:
                            "bold",
                        fontSize: "18px",
                        cursor: "pointer",
                    }}
                >
                    Подтвердить
                </button>
                <p
                    style={{
                        marginTop: "20px",
                        color: "#D6EAF8",
                    }}
                >
                    {timer > 0 ? (
                        `Отправить код повторно через ${timer} сек`
                    ) : (
                        <span
                            onClick={resendCode}
                            style={{
                                cursor: "pointer",
                                color: "#38BDF8",
                                fontWeight: "bold",
                            }}
                        >
                            Отправить новый код
                        </span>
                    )}
                </p>
            </div>
        </div>
    );
}

export default VerifyEmail;