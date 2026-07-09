import { useEffect, useState } from "react";
import TopNavigation from "../components/TopNavigation";
import PageContainer from "../components/PageContainer";
import PageHeader from "../components/PageHeader";
import ProfileCard from "../components/ProfileCard";
import Toast from "../components/Toast";

function Profile() {
    const [user, setUser] =
        useState(null);
    
    const [selectedAvatar, setSelectedAvatar] = useState(null);

    const [toast, setToast] = useState({
        show: false,
        type: "success",
        title: "",
        message: "",
    });

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
        };

        const showToast = (
                type,
                title,
                message
            ) => {

                setToast({
                    show: true,
                    type,
                    title,
                    message,
                });

                setTimeout(() => {
                    setToast((prev) => ({
                        ...prev,
                        show: false,
                    }));
                }, 3000);

            };

        const saveAvatar = async () => {

            if (!selectedAvatar?.file) {
                showToast(
                    "info",
                    "Внимание",
                    "Сначала выберите фотографию"
                );
                return;
            }

            try {

                const token = localStorage.getItem("token");

                const formData = new FormData();

                formData.append(
                    "avatar",
                    selectedAvatar.file
                );

                const response = await fetch(
                    "http://127.0.0.1:8000/update-avatar",
                    {
                        method: "POST",
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                        body: formData,
                    }
                );

                const data = await response.json();

                if (!response.ok) {
                    showToast(
                        "error",
                        "Ошибка",
                        data.message || "Не удалось загрузить фотографию"
                    );
                    return;
                }

                showToast(
                    "success",
                    "Успешно",
                    "Аватар обновлён"
                );

                await loadProfile();

                setSelectedAvatar(null);

            } catch (error) {

                console.error(error);

                showToast(
                    "error",
                    "Ошибка",
                    "Не удалось загрузить фотографию"
                );

            }

        };

    return (
        <>

            <div
                style={{
                    minHeight: "100vh",
                    background: "#061A40",
                }}
            >
                <TopNavigation />

                <PageContainer>

                    <PageHeader
                        title="Профиль"
                        subtitle="Управление аккаунтом"
                    />

                    <ProfileCard
                        user={user}
                        selectedAvatar={selectedAvatar}
                        setSelectedAvatar={setSelectedAvatar}
                        saveAvatar={saveAvatar}
                        logout={() => {
                            localStorage.removeItem("token");
                            window.location.href = "/";
                        }}
                    />

                </PageContainer>

            </div>

            <Toast
                show={toast.show}
                type={toast.type}
                title={toast.title}
                message={toast.message}
            />
        </>
    );
}

export default Profile;