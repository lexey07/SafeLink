import "./ProfileCard.css";

function ProfileCard({
    user,
    selectedAvatar,
    setSelectedAvatar,
    saveAvatar,
    logout,
}) {
    if (!user) {
        return null;
    }

    const handleAvatarChange = (event) => {

        const file = event.target.files[0];

        if (!file) return;

        const preview = URL.createObjectURL(file);

        setSelectedAvatar({
            file,
            preview,
        });

    };

    return (
        <div className="profile-card">

            <img
                className="profile-avatar"
                src={
                    selectedAvatar?.preview ||
                    (user.avatar
                        ? `http://127.0.0.1:8000${user.avatar}`
                        : "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
                }
                alt=""
            />

            <h2 className="profile-name">
                {user.nickname}
            </h2>

            <p className="profile-email">
                {user.email}
            </p>

            <div className="profile-actions">

                <label className="profile-button">

                    📁 Выбрать фотографию

                    <input
                        type="file"
                        accept="image/*"
                        hidden
                        onChange={handleAvatarChange}
                    />

                </label>

                <button
                    className="profile-button save"
                    onClick={saveAvatar}
                >
                    💾 Сохранить
                </button>

                <button
                    className="profile-button logout"
                    onClick={logout}
                >
                    ↩ Выйти
                </button>

            </div>

            <div className="profile-stats">

                <div className="profile-stat">

                    <div className="profile-stat-icon">
                        🐟
                    </div>

                    <div className="profile-stat-title">
                        Проверок
                    </div>

                    <div className="profile-stat-value">
                        {user.checks_left}
                    </div>

                </div>

                <div className="profile-stat">

                    <div className="profile-stat-icon">
                        👑
                    </div>

                    <div className="profile-stat-title">
                        Premium
                    </div>

                    <div className="profile-stat-value">
                        {user.is_premium
                            ? "Активен"
                            : "Не активен"}
                    </div>

                </div>

            </div>

        </div>
    );
}

export default ProfileCard;