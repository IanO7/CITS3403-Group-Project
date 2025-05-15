document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.animated-bar').forEach(function(bar) {
        const target = parseFloat(bar.getAttribute('data-target')) || 0;
        bar.style.transition = 'none';
        bar.style.width = '0%';
        void bar.offsetWidth; // Force reflow
        bar.style.transition = 'width 1.2s cubic-bezier(.4,2,.6,1)';
        setTimeout(() => {
            bar.style.width = target + '%';
        }, 100);
    });
});