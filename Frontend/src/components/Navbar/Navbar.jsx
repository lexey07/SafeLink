import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import logo from "../../assets/logo.png";
import "./Navbar.css";

function Navbar() {
    const [user, setUser] = useState(null);

    useEffect(() => {
        loadUser();
    }, []);

    const loadUser = async () => {
        const token = localStorage.getItem("token");

        if (!token) return;

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/me",
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            const data = await response.json();

            setUser(data);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <header className="navbar">
            <Link
                to="/dashboard"
                className="navbar-logo"
            >
                <div className="navbar-brand">
                    <img
                        src={logo}
                        alt="SafeLink"
                    />

                    <span className="navbar-title">
                        SafeLink
                    </span>
                </div>
            </Link>

            <div className="navbar-right">
                <button className="premium-button">
                    👑 Premium
                </button>

                <Link
                    to="/profile"
                    className="profile-link"
                >
                    <img
                        className="profile-avatar"
                        src={
                            user?.avatar ||
                            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                        }
                        alt="Профиль"
                    />

                    <span className="profile-name">
                        {user?.nickname || "Профиль"}
                    </span>
                </Link>
            </div>
        </header>
    );
}

export default Navbar;