document.querySelectorAll('.radio-input').forEach((container) => {
    const radios = container.querySelectorAll('input[type="radio"]');
    const selection = container.querySelector('.selection');

    radios.forEach((radio, index) => {
        radio.addEventListener('change', () => {
            const selectionWidth = 100 / radios.length;
            const selectionOffset = selectionWidth * index;
            selection.style.width = `${selectionWidth}%`;
            selection.style.transform = `translateX(${selectionOffset}%)`;
        });
    });
});