document.addEventListener("DOMContentLoaded", function() {
    const originalTextArea = document.getElementById("originalText");
    const translateButton = document.querySelector("button[class='bg-[#83ccb4]']");
    const translatedTextArea = document.getElementById("translatedText");
    const summeryButton = document.querySelector("button[class='bg-[#9dd7c3]']");
    const summmerizedTextArea = document.getElementById("summaryText");

    // 1. 번역하기
    translateButton.addEventListener("click", function() {
        if (originalTextArea.value.length > 4000) {
            alert('입력 가능한 최대 글자 수는 4000자입니다. 글자를 줄여주세요.');
            return;
        }

        fetch('/translate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                source_language: 'English',
                target_language: 'Korean',
                english_text: originalTextArea.value
            })
        })
        .then(response => response.json())
        .then(data => {
            translatedTextArea.innerText = data.translated_text;
            originalTextArea.setAttribute("readonly", true);
            originalTextArea.style.backgroundColor = "#f3f3f3";
        })
        .catch(error => console.error('Error:', error));
    });

    // 3. 요약하기
    summeryButton.addEventListener("click", function() {
        fetch('/summarize_text/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ english_text: translatedTextArea.innerText })
        })
        .then(response => response.json())
        .then(data => {
            summmerizedTextArea.innerText = data.summary;  // 서버 응답의 키 이름과 맞춰야 함
        })
        .catch(error => console.error('Error:', error));
    });
});