import { NavLink } from "react-router-dom";
import {
    House,
    History,
    Crown,
    User
} from "lucide-react";

import "./TopNavigation.css";

function TopNavigation() {

    const getClassName = ({ isActive }) =>
        isActive
            ? "top-nav-link active"
            : "top-nav-link";

    return (
        <nav className="top-navigation">

            <NavLink
                to="/dashboard"
                className={getClassName}
            >
                <House size={22} />
                <span>Главная</span>
            </NavLink>

            <NavLink
                to="/history"
                className={getClassName}
            >
                <History size={22} />
                <span>История</span>
            </NavLink>

            <NavLink
                to="/premium"
                className={getClassName}
            >
                <Crown size={22} />
                <span>Premium</span>
            </NavLink>

            <NavLink
                to="/profile"
                className={getClassName}
            >
                <User size={22} />
                <span>Профиль</span>
            </NavLink>

        </nav>
    );
}

export default TopNavigation;