document.addEventListener('DOMContentLoaded', function() {
    
    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking a link
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            menuToggle.classList.remove('active');
        });
    });
    
    // Certificate modal functionality
    const modalOverlay = document.getElementById('certificate-modal');
    const modalClose = document.querySelector('.modal-close');
    const internshipCards = document.querySelectorAll('.internship-card, .certification-card');
    const modalTitle = document.getElementById('modal-cert-title');
    const certificatePreview = document.getElementById('certificate-preview');
    
    // Open modal when clicking on internship or certification cards
    internshipCards.forEach(card => {
        card.addEventListener('click', function() {
            const title = this.querySelector('.internship-title, .certification-title').textContent;
            const certificateImage = this.dataset.image || `./assets/images/certificates/${this.dataset.certificate}.jpg`;
            
            modalTitle.textContent = `${title} - Certificate`;
            
            // Create image element with error handling
            const img = document.createElement('img');
            img.src = certificateImage;
            img.alt = `${title} Certificate`;
            img.className = 'certificate-image';
            img.onerror = function() {
                certificatePreview.innerHTML = `
                    <div class="certificate-placeholder">
                        <i class="fas fa-file-certificate"></i>
                        <p>Certificate image not found</p>
                        <p class="certificate-note">Please ensure the file exists at:<br>${certificateImage}</p>
                        <p class="certificate-note">File name should match exactly</p>
                    </div>
                `;
            };
            
            // Clear previous content and add new image
            certificatePreview.innerHTML = '';
            certificatePreview.appendChild(img);
            
            modalOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });
    
    // Close modal when clicking close button
    modalClose.addEventListener('click', function() {
        modalOverlay.classList.remove('active');
        document.body.style.overflow = 'auto';
    });
    
    // Close modal when clicking outside the modal content
    modalOverlay.addEventListener('click', function(e) {
        if (e.target === modalOverlay) {
            modalOverlay.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
            modalOverlay.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    });
    
    // Form submission handling
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Simple validation
            if (!data.name || !data.email || !data.message) {
                alert('Please fill in all fields.');
                return;
            }
            
            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(data.email)) {
                alert('Please enter a valid email address.');
                return;
            }
            
            // In a real implementation, you would send this data to a server
            // For demo purposes, we'll just show an alert
            alert(`Thank you for your message, ${data.name}! I'll get back to you soon at ${data.email}.`);
            
            // Reset the form
            this.reset();
        });
    }
    
    // Navbar scroll effect
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        
        // Add shadow when scrolled
        if (scrollTop > 50) {
            navbar.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.2)';
        } else {
            navbar.style.boxShadow = 'none';
        }
        
        lastScrollTop = scrollTop;
        
        // Update active nav link
        updateActiveNavLink();
        
        // Trigger scroll animations
        triggerScrollAnimations();
    });
    
    // Update active navigation link
    function updateActiveNavLink() {
        const sections = document.querySelectorAll('section');
        const navLinks = document.querySelectorAll('.nav-menu a');
        
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').substring(1) === current) {
                link.classList.add('active');
            }
        });
    }
    
    // Scroll animations
    function triggerScrollAnimations() {
        const sections = document.querySelectorAll('.section');
        
        sections.forEach(section => {
            const sectionTop = section.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (sectionTop < windowHeight * 0.85) {
                section.classList.add('visible');
                
                // Stagger animation for grid items
                const gridItems = section.querySelectorAll('.internship-card, .certification-card, .project-card, .skill-category, .education-card');
                gridItems.forEach((item, index) => {
                    item.style.transitionDelay = `${index * 0.1}s`;
                });
            }
        });
    }
    
    // Initialize animations on page load
    setTimeout(() => {
        triggerScrollAnimations();
    }, 300);
    
    // Add CSS for active nav link
    const style = document.createElement('style');
    style.textContent = `
        .nav-menu a.active {
            color: var(--accent-primary) !important;
        }
        
        .nav-menu a.active::after {
            width: 100% !important;
        }
        
        /* Add smooth transitions for grid items */
        .internship-card,
        .certification-card,
        .project-card,
        .skill-category,
        .education-card {
            transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
    `;
    document.head.appendChild(style);
    
    // Initialize active state for home link
    const homeLink = document.querySelector('.nav-menu a[href="#home"]');
    if (homeLink) {
        homeLink.classList.add('active');
    }
    
    // Profile image error handling enhancement
    const profileImage = document.querySelector('.profile-image');
    if (profileImage) {
        profileImage.addEventListener('error', function() {
            // If both images fail, show icon
            if (this.src.includes('profile-backup.jpg')) {
                this.style.display = 'none';
                const placeholder = document.createElement('div');
                placeholder.className = 'profile-placeholder';
                placeholder.innerHTML = '<i class="fas fa-user-circle"></i>';
                this.parentElement.appendChild(placeholder);
            }
        });
    }
    
    // Print current year in footer
    const currentYear = new Date().getFullYear();
    const footerText = document.querySelector('.footer-text');
    if (footerText) {
        footerText.textContent = `© ${currentYear} Aravind Adityaa. All rights reserved.`;
    }
});