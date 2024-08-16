document.addEventListener("DOMContentLoaded", function() {
    const originalTextArea = document.getElementById("originalText");
    const translateButton = document.querySelector("button[class*='bg-[#83ccb4]']");
    const wordExplanation = document.getElementById("wordExplanation");
    const translatedTextArea = document.getElementById("translatedText");
    const summeryButton = document.querySelector("button[class*='bg-[#9dd7c3]']");
    const summmerizedTextArea = document.getElementById("summaryText");

    // 1. 텍스트 영역 잠금
    translateButton.addEventListener("click", function() {
        originalTextArea.setAttribute("readonly", true); 
        originalTextArea.style.backgroundColor = "#f3f3f3"; 
        if (originalTextArea.value.length > 4000) {
            alert('입력 가능한 최대 글자 수는 4000자입니다. 글자를 줄여주세요.');
            return;
        }
        // 원문을 번역으로 단순 복사하는 임시 코드
        translatedTextArea.innerText = originalTextArea.value;
    });

    // 2. 어휘 설명
    translatedTextArea.addEventListener("mouseup", function() {
        const selection = window.getSelection().toString().trim();
        if (selection) {
            const explanation = `${selection}: 어휘 설명이 표시됩니다.`;
            wordExplanation.innerText += explanation + "\n";
        }
    });

    //3. 요악문 출력 
    summeryButton.addEventListener("click", function() {
        // 원문을 요약으로 단순 복사하는 임시 코드
        summmerizedTextArea.innerText = originalTextArea.value;
    });


});