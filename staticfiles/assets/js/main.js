/**
* Template Name: MediTrust
* Template URL: https://bootstrapmade.com/meditrust-bootstrap-hospital-website-template/
* Updated: Jul 04 2025 with Bootstrap v5.3.7
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Init isotope layout and filters
   */
  document.querySelectorAll('.isotope-layout').forEach(function(isotopeItem) {
    let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
    let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
    let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

    let initIsotope;
    imagesLoaded(isotopeItem.querySelector('.isotope-container'), function() {
      initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
        itemSelector: '.isotope-item',
        layoutMode: layout,
        filter: filter,
        sortBy: sort
      });
    });

    isotopeItem.querySelectorAll('.isotope-filters li').forEach(function(filters) {
      filters.addEventListener('click', function() {
        isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
        this.classList.add('filter-active');
        initIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        if (typeof aosInit === 'function') {
          aosInit();
        }
      }, false);
    });

  });

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Frequently Asked Questions Toggle
   */
  document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle, .faq-item .faq-header').forEach((faqItem) => {
    faqItem.addEventListener('click', () => {
      faqItem.parentNode.classList.toggle('faq-active');
    });
  });

  /**
   * Insurance Slider Functionality
   */
  class InsuranceSlider {
    constructor() {
      this.slider = document.getElementById('insuranceSlider');
      this.slides = this.slider?.querySelectorAll('.insurance-slide');
      this.currentIndex = 0;
      this.slideWidth = 230; // 200px width + 30px margin
      this.autoplayDelay = 2000; // 2 seconds per slide
      this.autoplayTimer = null;
      this.totalSlides = 0;
      
      if (this.slider && this.slides.length > 0) {
        this.init();
      }
    }

    init() {
      this.totalSlides = this.slides.length;
      
      // Clone slides for infinite effect
      this.cloneSlides();
      
      // Start autoplay
      this.startAutoplay();
      
      // Pause on hover
      this.slider.addEventListener('mouseenter', () => this.pauseAutoplay());
      this.slider.addEventListener('mouseleave', () => this.startAutoplay());
      
      // Touch events for mobile
      this.addTouchEvents();
    }

    cloneSlides() {
      const slidesArray = Array.from(this.slides);
      
      // Clone slides and append to the end
      slidesArray.forEach(slide => {
        const clone = slide.cloneNode(true);
        this.slider.appendChild(clone);
      });
    }

    next() {
      this.currentIndex++;
      this.updateSliderPosition();
      
      // Reset to beginning when reaching the end of original slides
      if (this.currentIndex >= this.totalSlides) {
        setTimeout(() => {
          this.slider.style.transition = 'none';
          this.currentIndex = 0;
          this.updateSliderPosition();
          setTimeout(() => {
            this.slider.style.transition = 'transform 0.5s ease-in-out';
          }, 50);
        }, 500);
      }
    }

    prev() {
      if (this.currentIndex <= 0) {
        this.slider.style.transition = 'none';
        this.currentIndex = this.totalSlides - 1;
        this.updateSliderPosition();
        setTimeout(() => {
          this.slider.style.transition = 'transform 0.5s ease-in-out';
        }, 50);
      } else {
        this.currentIndex--;
        this.updateSliderPosition();
      }
    }

    updateSliderPosition() {
      const translateX = -this.currentIndex * this.slideWidth;
      this.slider.style.transform = `translateX(${translateX}px)`;
    }

    startAutoplay() {
      this.pauseAutoplay();
      this.autoplayTimer = setInterval(() => {
        this.next();
      }, this.autoplayDelay);
    }

    pauseAutoplay() {
      if (this.autoplayTimer) {
        clearInterval(this.autoplayTimer);
        this.autoplayTimer = null;
      }
    }

    addTouchEvents() {
      let startX = 0;
      let startY = 0;
      let endX = 0;
      let endY = 0;

      this.slider.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
        this.pauseAutoplay();
      });

      this.slider.addEventListener('touchmove', (e) => {
        endX = e.touches[0].clientX;
        endY = e.touches[0].clientY;
      });

      this.slider.addEventListener('touchend', (e) => {
        const diffX = startX - endX;
        const diffY = startY - endY;
        
        // Only trigger swipe if horizontal movement is greater than vertical
        if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
          if (diffX > 0) {
            this.next();
          } else {
            this.prev();
          }
        }
        
        this.startAutoplay();
      });
    }
  }

  // Initialize insurance slider when DOM is loaded (disabled for CSS animation)
  // document.addEventListener('DOMContentLoaded', function() {
  //   window.insuranceSlider = new InsuranceSlider();
  // });

})();