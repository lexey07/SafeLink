export async function checkUrl(url, token) {
    const response = await fetch(
        "http://127.0.0.1:8000/check-url",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                url,
            }),
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || data.message || "Ошибка сервера"
        );
    }

    return data;
}