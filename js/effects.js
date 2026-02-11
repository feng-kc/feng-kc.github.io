// ==================== 烟花波纹效果 ====================
class RippleEffect {
  constructor() {
    this.ripples = [];
    this.colors = ['#e8c4a0', '#d4a574', '#c9b896', '#e6d5b8', '#f0e6d2'];
    this.init();
  }

  init() {
    document.addEventListener('click', (e) => this.createRipple(e));
    this.animate();
  }

  createRipple(e) {
    const x = e.clientX;
    const y = e.clientY;
    const color = this.colors[Math.floor(Math.random() * this.colors.length)];
    
    // 创建主波纹
    for (let i = 0; i < 5; i++) {
      this.ripples.push({
        x: x,
        y: y,
        radius: 0,
        maxRadius: 100 + Math.random() * 100,
        color: color,
        alpha: 1,
        lineWidth: 2 + Math.random() * 2,
        speed: 2 + Math.random() * 2
      });
    }

    // 创建粒子效果
    for (let i = 0; i < 20; i++) {
      const angle = (Math.PI * 2 / 20) * i;
      const speed = 3 + Math.random() * 3;
      this.ripples.push({
        x: x,
        y: y,
        radius: 0,
        maxRadius: 20 + Math.random() * 20,
        color: color,
        alpha: 1,
        lineWidth: 1,
        speed: speed,
        angle: angle,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        isParticle: true
      });
    }
  }

  animate() {
    const canvas = document.getElementById('ripple-canvas');
    if (!canvas) {
      this.createCanvas();
      return;
    }

    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 更新和绘制波纹
    for (let i = this.ripples.length - 1; i >= 0; i--) {
      const ripple = this.ripples[i];
      
      if (ripple.isParticle) {
        // 粒子效果
        ripple.x += ripple.vx;
        ripple.y += ripple.vy;
        ripple.radius += 0.5;
        ripple.alpha -= 0.02;
        
        ctx.beginPath();
        ctx.arc(ripple.x, ripple.y, ripple.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.hexToRgba(ripple.color, ripple.alpha);
        ctx.fill();
      } else {
        // 波纹效果
        ripple.radius += ripple.speed;
        ripple.alpha -= 0.02;
        
        ctx.beginPath();
        ctx.arc(ripple.x, ripple.y, ripple.radius, 0, Math.PI * 2);
        ctx.strokeStyle = this.hexToRgba(ripple.color, ripple.alpha);
        ctx.lineWidth = ripple.lineWidth;
        ctx.stroke();
      }

      if (ripple.alpha <= 0) {
        this.ripples.splice(i, 1);
      }
    }

    requestAnimationFrame(() => this.animate());
  }

  createCanvas() {
    const canvas = document.createElement('canvas');
    canvas.id = 'ripple-canvas';
    canvas.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      pointer-events: none;
      z-index: 9999;
    `;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    document.body.appendChild(canvas);
    
    window.addEventListener('resize', () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });
    
    this.animate();
  }

  hexToRgba(hex, alpha) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }
}

// ==================== 星星拖尾效果 ====================
class StarTrail {
  constructor() {
    this.stars = [];
    this.mouseX = 0;
    this.mouseY = 0;
    this.init();
  }

  init() {
    document.addEventListener('mousemove', (e) => {
      this.mouseX = e.clientX;
      this.mouseY = e.clientY;
      this.createStar();
    });
    this.animate();
  }

  createStar() {
    if (this.stars.length > 50) {
      this.stars.shift();
    }

    this.stars.push({
      x: this.mouseX + (Math.random() - 0.5) * 20,
      y: this.mouseY + (Math.random() - 0.5) * 20,
      size: 2 + Math.random() * 3,
      alpha: 1,
      rotation: Math.random() * Math.PI * 2,
      rotationSpeed: (Math.random() - 0.5) * 0.1,
      color: this.getRandomColor()
    });
  }

  getRandomColor() {
    const colors = ['#FFD700', '#FFA500', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'];
    return colors[Math.floor(Math.random() * colors.length)];
  }

  animate() {
    const canvas = document.getElementById('star-canvas');
    if (!canvas) {
      this.createCanvas();
      return;
    }

    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = this.stars.length - 1; i >= 0; i--) {
      const star = this.stars[i];
      star.alpha -= 0.02;
      star.rotation += star.rotationSpeed;

      if (star.alpha <= 0) {
        this.stars.splice(i, 1);
        continue;
      }

      ctx.save();
      ctx.translate(star.x, star.y);
      ctx.rotate(star.rotation);
      ctx.globalAlpha = star.alpha;

      // 绘制星星
      ctx.beginPath();
      const spikes = 5;
      const outerRadius = star.size;
      const innerRadius = star.size / 2;

      for (let j = 0; j < spikes * 2; j++) {
        const radius = j % 2 === 0 ? outerRadius : innerRadius;
        const angle = (j * Math.PI) / spikes;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        if (j === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }

      ctx.closePath();
      ctx.fillStyle = star.color;
      ctx.fill();

      // 添加发光效果
      ctx.shadowColor = star.color;
      ctx.shadowBlur = 10;
      ctx.fill();

      ctx.restore();
    }

    requestAnimationFrame(() => this.animate());
  }

  createCanvas() {
    const canvas = document.createElement('canvas');
    canvas.id = 'star-canvas';
    canvas.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      pointer-events: none;
      z-index: 9998;
    `;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    document.body.appendChild(canvas);
    
    window.addEventListener('resize', () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });
    
    this.animate();
  }
}

// ==================== 主题切换（带动画和持久化） ====================
function initThemeToggle() {
  const toggleBtn = document.querySelector('.theme-toggle');
  if (!toggleBtn) return;

  // 从localStorage读取主题状态
  let isDark = localStorage.getItem('theme') === 'dark';
  document.body.classList.toggle('dark', isDark);
  toggleBtn.textContent = isDark ? '☀️ 亮色' : '🌙 暗色';

  // 创建全屏切换遮罩
  const themeOverlay = document.createElement('div');
  themeOverlay.className = 'theme-overlay';
  themeOverlay.innerHTML = `
    <div class="theme-transition">
      <i class="fa-solid fa-moon"></i>
    </div>
  `;
  document.body.appendChild(themeOverlay);

  toggleBtn.addEventListener('click', () => {
    // 显示全屏切换动画
    themeOverlay.classList.add('active');

    setTimeout(() => {
      isDark = !isDark;
      document.body.classList.toggle('dark', isDark);
      toggleBtn.textContent = isDark ? '☀️ 亮色' : '🌙 暗色';
      localStorage.setItem('theme', isDark ? 'dark' : 'light');

      // 更新遮罩图标
      const icon = themeOverlay.querySelector('i');
      icon.className = isDark ? 'fa-solid fa-sun' : 'fa-solid fa-moon';

      // 1-2秒后隐藏遮罩
      setTimeout(() => {
        themeOverlay.classList.remove('active');
      }, 1500);
    }, 250);
  });
}

// ==================== 页面进入动画 ====================
function initPageAnimations() {
  // 检查是否首次访问
  const hasVisited = localStorage.getItem('blogVisited');
  const heroSection = document.querySelector('.hero-section');

  // 如果是首次访问，显示Hero；否则隐藏
  if (!hasVisited) {
    // 首次访问，设置标志位
    localStorage.setItem('blogVisited', 'true');
    initTypewriter();
  } else {
    // 已访问过，直接隐藏Hero
    if (heroSection) {
      heroSection.classList.add('hidden');
    }
  }

  // 点击进入按钮后隐藏Hero
  const enterBtn = document.querySelector('.enter-btn');
  if (enterBtn) {
    enterBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const heroSection = document.querySelector('.hero-section');
      if (heroSection) {
        heroSection.classList.add('hidden');
      }
      const mainContent = document.querySelector('#main-content');
      if (mainContent) {
        mainContent.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  // 所有元素从上方浮入动画（不包括hero-section）
  const animatedElements = document.querySelectorAll(
    '.article-card, .article-full, .section-title, ' +
    '.profile-card, .stats, .quick-links, .random-post, .tags-cloud, .welcome-card'
  );

  animatedElements.forEach((el, index) => {
    el.classList.add('fade-in-section');
    el.classList.add(`delay-${(index % 5) + 1}`);
  });

  // 使用IntersectionObserver触发动画
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });

  animatedElements.forEach(el => {
    observer.observe(el);
  });
}

// ==================== 打字机效果 ====================
function initTypewriter() {
  const element = document.querySelector('.hero-typewriter');
  if (!element) return;

  const text = element.getAttribute('data-text');
  element.textContent = '';
  let index = 0;

  function type() {
    if (index < text.length) {
      element.textContent += text.charAt(index);
      index++;
      setTimeout(type, 100);
    }
  }

  // 延迟一点开始打字
  setTimeout(type, 500);
}

// ==================== 初始化 ====================
document.addEventListener('DOMContentLoaded', () => {
  new RippleEffect();
  new StarTrail();
  initThemeToggle();
  initPageAnimations();
});
