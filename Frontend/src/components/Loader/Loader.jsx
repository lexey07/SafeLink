import "./Loader.css";

function Loader() {
    return (
        <div className="loader-container">
            <div className="loader"></div>

            <p className="loader-text">
                Загрузка истории...
            </p>
        </div>
    );
}

export default Loader;