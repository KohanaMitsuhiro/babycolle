window.addEventListener('DOMContentLoaded', (event) => {
    console.log('ページが読み込まれました');
    adjustButtonPosition();
    const images = ['image1.png', 'image2.png', 'image3.png'];
    let currentImageIndex = 0;

    setInterval(() => {
        currentImageIndex = (currentImageIndex + 1) % images.length;
        document.getElementById('mainImage').src = images[currentImageIndex];
    }, 5000); // 5000ミリ秒（5秒）ごとに画像を切り替え

    document.getElementById('arrowPrev').addEventListener('click', () => {
        currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
        document.getElementById('mainImage').src = images[currentImageIndex];
    });

    document.getElementById('arrowNext').addEventListener('click', () => {
        currentImageIndex = (currentImageIndex + 1) % images.length;
        document.getElementById('mainImage').src = images[currentImageIndex];
    });
});

window.addEventListener('resize', adjustButtonPosition);

function adjustButtonPosition() {
    const footerHeight = document.querySelector('footer').offsetHeight;
    const conversionButton = document.querySelector('#conversionButton');
    conversionButton.style.bottom = `${footerHeight + 20}px`;  // 20 is the desired gap between the button and the footer
}

document.getElementById('hamburger-menu').addEventListener('click', function() {
    var navMenu = document.getElementById('nav-menu');
    if (navMenu.style.display === 'none' || navMenu.style.display === '') {
        navMenu.style.display = 'flex';
    } else {
        navMenu.style.display = 'none';
    }
});

document.getElementById('close-button').addEventListener('click', function() {
    document.getElementById('nav-menu').style.display = 'none';
});