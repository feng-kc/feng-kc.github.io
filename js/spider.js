// ==================== 蜘蛛网特效 ====================
class SpiderWeb {
  constructor() {
    this.particles = [];
    this.canvas = null;
    this.ctx = null;
    this.width = 0;
    this.height = 0;
    this.particleCount = 80;
    this.connectionDistance = 150;
    this.mouseDistance = 200;
    this.mouseX = 0;
    this.mouseY = 0;
    
    this.init();
  }

  init() {
    this.createCanvas();
    this.initParticles();
    this.addEventListeners();
    this.animate();
  }

  createCanvas() {
    this.canvas = document.getElementById('spider-canvas');
    if (!this.canvas) {
      this.canvas = document.createElement('canvas');
      this.canvas.id = 'spider-canvas';
      this.canvas.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        pointer-events: none;
        z-index: 9997;
        opacity: 0.6;
      `;
      document.body.appendChild(this.canvas);
    }
    
    this.ctx = this.canvas.getContext('2d');
    this.resizeCanvas();
  }

  resizeCanvas() {
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    this.canvas.width = this.width;
    this.canvas.height = this.height;
  }

  initParticles() {
    this.particles = [];
    
    for (let i = 0; i < this.particleCount; i++) {
      this.particles.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: 1 + Math.random() * 2,
        color: this.getRandomColor()
      });
    }
  }

  getRandomColor() {
    const colors = ['#e8c4a0', '#d4a574', '#c9b896', '#e6d5b8', '#f0e6d2'];
    return colors[Math.floor(Math.random() * colors.length)];
  }

  addEventListeners() {
    window.addEventListener('resize', () => {
      this.resizeCanvas();
      this.initParticles();
    });

    window.addEventListener('mousemove', (e) => {
      this.mouseX = e.clientX;
      this.mouseY = e.clientY;
    });
  }

  updateParticles() {
    for (let i = 0; i < this.particles.length; i++) {
      const particle = this.particles[i];
      
      // 更新位置
      particle.x += particle.vx;
      particle.y += particle.vy;
      
      // 边界检测
      if (particle.x < 0 || particle.x > this.width) {
        particle.vx *= -1;
      }
      if (particle.y < 0 || particle.y > this.height) {
        particle.vy *= -1;
      }
      
      // 鼠标交互
      const dx = this.mouseX - particle.x;
      const dy = this.mouseY - particle.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < this.mouseDistance) {
        const force = (this.mouseDistance - distance) / this.mouseDistance;
        particle.x -= dx * force * 0.02;
        particle.y -= dy * force * 0.02;
      }
    }
  }

  drawParticles() {
    for (let i = 0; i < this.particles.length; i++) {
      const particle = this.particles[i];
      
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      this.ctx.fillStyle = particle.color;
      this.ctx.fill();
    }
  }

  drawConnections() {
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const dx = this.particles[i].x - this.particles[j].x;
        const dy = this.particles[i].y - this.particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < this.connectionDistance) {
          const opacity = 1 - (distance / this.connectionDistance);
          this.ctx.beginPath();
          this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
          this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
          this.ctx.strokeStyle = `rgba(212, 165, 116, ${opacity * 0.3})`;
          this.ctx.lineWidth = 0.5;
          this.ctx.stroke();
        }
      }
    }
  }

  drawMouseConnections() {
    for (let i = 0; i < this.particles.length; i++) {
      const dx = this.mouseX - this.particles[i].x;
      const dy = this.mouseY - this.particles[i].y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < this.mouseDistance) {
        const opacity = 1 - (distance / this.mouseDistance);
        this.ctx.beginPath();
        this.ctx.moveTo(this.mouseX, this.mouseY);
        this.ctx.lineTo(this.particles[i].x, this.particles[i].y);
        this.ctx.strokeStyle = `rgba(212, 165, 116, ${opacity * 0.5})`;
        this.ctx.lineWidth = 1;
        this.ctx.stroke();
      }
    }
  }

  animate() {
    this.ctx.clearRect(0, 0, this.width, this.height);
    
    this.updateParticles();
    this.drawConnections();
    this.drawMouseConnections();
    this.drawParticles();
    
    requestAnimationFrame(() => this.animate());
  }
}

// 初始化蜘蛛网特效
document.addEventListener('DOMContentLoaded', () => {
  new SpiderWeb();
});
