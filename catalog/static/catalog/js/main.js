/* ============================================================
   KAM MÜZİK — Ana JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    /* ---------- AOS: scroll reveal animasyonları ---------- */
    if (window.AOS) {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,        // her öğe bir kez animasyon oynasın
            offset: 80,
        });
    }

    /* ---------- Navbar: sayfa kaydırılınca koyulaş ---------- */
    const navbar = document.getElementById('navbar');
    const onScroll = () => {
        if (window.scrollY > 40) navbar.classList.add('scrolled');
        else navbar.classList.remove('scrolled');
    };
    window.addEventListener('scroll', onScroll);
    onScroll();

    /* ---------- Mobil menü aç/kapat ---------- */
    const toggle = document.getElementById('navToggle');
    const menu = document.getElementById('navMenu');
    if (toggle && menu) {
        toggle.addEventListener('click', () => menu.classList.toggle('open'));
        // menüden bir linke tıklanınca kapat
        menu.querySelectorAll('.navbar__link').forEach(link =>
            link.addEventListener('click', () => menu.classList.remove('open'))
        );
    }

    /* ---------- GSAP: hero giriş animasyonu ---------- */
    if (window.gsap) {
        const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
        tl.from('.hero__title', { y: 40, opacity: 0, duration: 1 })
          .from('.hero__subtitle', { y: 30, opacity: 0, duration: 0.8 }, '-=0.5')
          .from('.hero__cta', { y: 20, opacity: 0, duration: 0.7 }, '-=0.4');
    }

});
