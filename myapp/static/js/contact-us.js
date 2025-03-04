document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menu-toggle');
    const navMenu = document.getElementById('nav-menu');
    const hamburger = document.querySelector('.hamburger');
  
    menuToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      hamburger.classList.toggle('open');
    });
  });
  