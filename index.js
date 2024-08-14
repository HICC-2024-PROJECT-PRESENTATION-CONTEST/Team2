document.addEventListener('DOMContentLoaded', function() {
    // Select the 'TXT로 변환하기' button using its class
    const txtButton = document.querySelector('p[style*="text-[#6eaa96]"]');
    
    if (txtButton) {
        txtButton.addEventListener('click', function() {
            window.location.href = 'text_tr_improved.html';  // Navigate to the text_tr.html page
        });
    }
});
