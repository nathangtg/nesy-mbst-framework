export function initNavigation() {
  const nav = document.getElementById('main-nav');
  const links = nav.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('main > section');

  // Highlight active nav link on scroll
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          links.forEach((link) => {
            link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
          });
        }
      });
    },
    {
      threshold: 0.3,
      rootMargin: '-80px 0px -50% 0px',
    }
  );

  sections.forEach((section) => observer.observe(section));

  // Shrink nav on scroll
  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;
    if (currentScroll > 100) {
      nav.classList.add('shadow-md');
    } else {
      nav.classList.remove('shadow-md');
    }
    lastScroll = currentScroll;
  });
}
