let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;

// Update slide counter display
function updateSlideCounter() {
    document.getElementById('current-slide').textContent = currentSlide + 1;
    document.getElementById('total-slides').textContent = totalSlides;
}

// Show specific slide
function showSlide(index) {
    // Hide all slides
    slides.forEach(slide => slide.classList.remove('active'));
    
    // Show the selected slide
    if (index >= 0 && index < totalSlides) {
        slides[index].classList.add('active');
        currentSlide = index;
        updateSlideCounter();
        updateNavButtons();
    }
}

// Next slide
function nextSlide() {
    if (currentSlide < totalSlides - 1) {
        showSlide(currentSlide + 1);
    }
}

// Previous slide
function previousSlide() {
    if (currentSlide > 0) {
        showSlide(currentSlide - 1);
    }
}

// Update navigation buttons state
function updateNavButtons() {
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    
    prevBtn.disabled = currentSlide === 0;
    nextBtn.disabled = currentSlide === totalSlides - 1;
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    switch(e.key) {
        case 'ArrowRight':
        case ' ': // Spacebar
            e.preventDefault();
            nextSlide();
            break;
        case 'ArrowLeft':
            e.preventDefault();
            previousSlide();
            break;
        case 'Home':
            e.preventDefault();
            showSlide(0);
            break;
        case 'End':
            e.preventDefault();
            showSlide(totalSlides - 1);
            break;
    }
});

// Touch/swipe support for mobile
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    const swipeThreshold = 50;
    const diff = touchStartX - touchEndX;
    
    if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
            // Swipe left - next slide
            nextSlide();
        } else {
            // Swipe right - previous slide
            previousSlide();
        }
    }
}

// Initialize
updateSlideCounter();
updateNavButtons();

// Add click handlers to navigation buttons
document.querySelector('.prev-btn').addEventListener('click', previousSlide);
document.querySelector('.next-btn').addEventListener('click', nextSlide);





