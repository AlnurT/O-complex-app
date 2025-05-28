document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("city-input");
    const prevCity = document.getElementById("prev-city");
    const suggestionsDiv = document.getElementById("suggestions");
    const button = document.getElementById("search-btn");
    const prevButton = document.getElementById("last-weather-btn");
    const resultDiv = document.getElementById("weather-result");

    let debounceTimeout = null;

    // Функция для получения подсказок городов
    input.addEventListener("input", () => {
        clearTimeout(debounceTimeout);
        const query = input.value.trim();
        if (query.length === 0) {
            suggestionsDiv.innerHTML = "";
            return;
        }
        debounceTimeout = setTimeout(() => {
            fetch(`/cities?city=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => {
                    suggestionsDiv.innerHTML = "";
                    data.forEach(city => {
                        const div = document.createElement("div");
                        div.textContent = city;
                        div.className = "suggestion-item";
                        div.addEventListener("click", () => {
                            input.value = city;
                            suggestionsDiv.innerHTML = "";
                        });
                        suggestionsDiv.appendChild(div);
                    });
                });
        }, 300); // задержка для уменьшения количества запросов
    });

    button.addEventListener("click", () => {
        const cityName = input.value.trim();
        if (!cityName) return;

        resultDiv.innerHTML = "Загружаю...";
        fetch(`/weather?city=${encodeURIComponent(cityName)}`)
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    resultDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
                } else {
                    resultDiv.innerHTML = `
                        <h2>Погода</h2>
                        <p>Страна: ${data.country}</p>
                        <p>Город: ${data.city}</p>
                        <p>Температура: ${data.temperature} °C</p>
                        <p>Скорость ветра: ${data.windspeed} км/ч</p>
                    `;
                }
            })
            .catch(() => {
                resultDiv.innerHTML = `<p style="color:red;">Ошибка при получении данных.</p>`;
            });
    });

    prevButton.addEventListener("click", () => {
        const cityName = prevCity.value;

        resultDiv.innerHTML = "Загружаю...";
        fetch(`/weather?city=${encodeURIComponent(cityName)}`)
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    resultDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
                } else {
                    resultDiv.innerHTML = `
                        <h3>Погода</h3>
                        <p>Страна: ${data.country}</p>
                        <p>Город: ${data.city}</p>
                        <p>Температура: ${data.temperature} °C</p>
                        <p>Скорость ветра: ${data.windspeed} км/ч</p>
                    `;
                }
            })
            .catch(() => {
                resultDiv.innerHTML = `<p style="color:red;">Ошибка при получении данных.</p>`;
            });
    });
});