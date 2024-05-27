function sendRequest() {
  // Путь к файлу на вашем локальном компьютере или сервере
  const url = "D:\Python\Music-Analyzer\site\slider2.html"; // Например, 'data.php' если это PHP файл

  // Данные для отправки на сервер
  const data = {
    slider1: document.getElementById('slider1').value,
    slider2: document.getElementById('slider2').value,
    slider3: document.getElementById('slider3').value,
    slider4: document.getElementById('slider4').value,
    slider5: document.getElementById('slider5').value
  };

  // Опции запроса
  const options = {
    method: 'POST', // Метод запроса
    headers: {
      'Content-Type': 'application/json' // Тип содержимого
    },
    body: JSON.stringify(data) // Преобразование данных в JSON формат
  };

  // Отправка запроса на сервер
  fetch(url, options)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // Преобразование ответа в JSON
    })
    .then(data => {
      // Обработка полученных данных
      console.log('Server response:', data);
      // Возможно, выполнение каких-то действий с полученными данными
    })
    .catch(error => {
      // Обработка ошибок
      console.error('There was a problem with the fetch operation:', error);
    });
}

// Получаем все слайдеры
const sliders = document.querySelectorAll('.slider');

// Обходим каждый слайдер
sliders.forEach(slider => {
  // Получаем элемент с соответствующим id для отображения значения
  const sliderValue = document.getElementById(slider.id + 'Value');

  // Обновляем значение при изменении положения слайдера
  slider.addEventListener('input', () => {
    sliderValue.textContent = slider.value;
  });
});



