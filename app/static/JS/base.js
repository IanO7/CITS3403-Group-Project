document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    const footer = document.querySelector('.footer');
    function onScroll() {
        // Get the bottom position of the viewport
        const scrollBottom = window.scrollY + window.innerHeight;
        // Get the top position of the footer
        const footerTop = footer ? footer.offsetTop : document.body.scrollHeight;
        // If not at the footer, keep transparent
        if (scrollBottom < footerTop) {
            navbar.classList.add('navbar-transparent');
        } else {
            navbar.classList.add('navbar-transparent');
        }
    }
    window.addEventListener('scroll', onScroll);
    onScroll(); // Set initial state
});