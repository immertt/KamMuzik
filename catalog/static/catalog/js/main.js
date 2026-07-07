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

    /* ---------- GSAP: hero giriş animasyonu (sadece anasayfada) ---------- */
    if (window.gsap && document.querySelector('.hero__title')) {
        const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
        tl.from('.hero__title', { y: 40, opacity: 0, duration: 1 })
          .from('.hero__subtitle', { y: 30, opacity: 0, duration: 0.8 }, '-=0.5')
          .from('.hero__cta', { y: 20, opacity: 0, duration: 0.7 }, '-=0.4');
    }
    
    /* ---------- Hero parallax (arka plan yavaş kayar) ---------- */
    if (window.gsap && window.ScrollTrigger && document.querySelector('.hero')) {
        gsap.registerPlugin(ScrollTrigger);

        const hero = document.querySelector('.hero');

        // Arka plan görseli sayfa kaydıkça yavaşça aşağı kaysın (derinlik)
        gsap.to(hero, {
            backgroundPositionY: "30%",
            ease: "none",
            scrollTrigger: {
                trigger: hero,
                start: "top top",
                end: "bottom top",
                scrub: true,
            }
        });

        // Hero içeriği (yazılar) kaydıkça hafif yukarı çıkıp solsun
        const heroContent = document.querySelector('.hero__content');
        if (heroContent) {
            gsap.to(heroContent, {
                y: -80,
                opacity: 0.3,
                ease: "none",
                scrollTrigger: {
                    trigger: hero,
                    start: "top top",
                    end: "bottom top",
                    scrub: true,
                }
            });
        }
    }
    
    /* ---------- Hero parçacıkları oluştur ---------- */
    const particleContainer = document.getElementById('heroParticles');
    if (particleContainer) {
        const count = 26;
        for (let i = 0; i < count; i++) {
            const p = document.createElement('span');
            p.className = 'particle';
            p.style.left = Math.random() * 100 + '%';
            p.style.animationDuration = (6 + Math.random() * 8) + 's';   // 6-14s arası
            p.style.animationDelay = (Math.random() * 8) + 's';
            const size = 2 + Math.random() * 3;                          // 2-5px
            p.style.width = size + 'px';
            p.style.height = size + 'px';
            particleContainer.appendChild(p);
        }
    }

    /* ---------- Yumuşak kaydırma (aynı sayfa + sayfalar arası) ---------- */
    const navHeight = 76;

    function smoothScrollTo(hash) {
        const target = document.querySelector(hash);
        if (!target) return;
        const top = target.getBoundingClientRect().top + window.scrollY - navHeight;
        window.scrollTo({ top: top, behavior: 'smooth' });
    }

    // 1) Aynı sayfadaki çapa linkleri (#... veya /#... ama mevcut sayfada)
    document.querySelectorAll('a[href*="#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            const url = new URL(this.href, window.location.origin);
            const samePage = (url.pathname === window.location.pathname);
            if (samePage && url.hash && document.querySelector(url.hash)) {
                e.preventDefault();
                smoothScrollTo(url.hash);
            }
            // farklı sayfaysa: tarayıcı normal gitsin, aşağıdaki kod devralır
        });
    });

    // 2) Başka sayfadan gelindiyse (adreste #hakkimizda gibi çapa varsa) o bölüme kay
    if (window.location.hash) {
        const hash = window.location.hash;
        // sayfa ve görseller yerleşsin diye küçük gecikme
        setTimeout(() => smoothScrollTo(hash), 300);
    }

    /* ---------- Lightbox (görsel büyütme) ---------- */
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightboxImg');
    const lightboxCaption = document.getElementById('lightboxCaption');
    const lightboxClose = document.getElementById('lightboxClose');

    if (lightbox) {
        // .lightbox-trigger sınıflı tüm görseller tıklanabilir
        document.querySelectorAll('.lightbox-trigger').forEach(img => {
            img.addEventListener('click', () => {
                const src = img.dataset.full || img.src;
                lightboxImg.src = src;
                lightboxImg.alt = img.alt || '';
                lightboxCaption.textContent = img.dataset.caption || img.alt || '';
                lightbox.classList.add('open');
                lightbox.setAttribute('aria-hidden', 'false');
                document.body.style.overflow = 'hidden';  // arka plan kaymasın
            });
        });

        const closeLightbox = () => {
            lightbox.classList.remove('open');
            lightbox.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        };

        lightboxClose.addEventListener('click', closeLightbox);
        // boş alana tıklayınca kapansın (görselin kendisine değil)
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) closeLightbox();
        });
        // ESC tuşu ile kapansın
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && lightbox.classList.contains('open')) closeLightbox();
        });
    }

});
