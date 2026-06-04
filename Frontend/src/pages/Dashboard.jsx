import { useState } from "react";

function Dashboard() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);

  const checkUrl = async () => {
    const token = localStorage.getItem("token");

    const response = await fetch(
      "http://127.0.0.1:8000/check-url",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          username: "lexey",
          url: url
        })
      }
    );

    const data = await response.json();
    console.log(data);
    setResult(data);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>Проверка URL</h1>

      <input
        type="text"
        placeholder="Введите ссылку"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <button onClick={checkUrl}>
        Проверить
      </button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>Результат</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default Dashboard;