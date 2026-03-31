'use client';
import { useEffect, useRef } from 'react';

export function Starfield() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let W = window.innerWidth;
    let H = window.innerHeight;
    canvas.width = W;
    canvas.height = H;

    // ── Stars ──────────────────────────────────────────────────────────────
    const STAR_COUNT = 220;
    const stars = Array.from({ length: STAR_COUNT }, () => ({
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 1.4 + 0.2,
      alpha: Math.random() * 0.7 + 0.2,
      speed: Math.random() * 0.012 + 0.003,
      phase: Math.random() * Math.PI * 2,
      color: ['#ffffff', '#93c5fd', '#c4b5fd', '#fbbf24'][Math.floor(Math.random() * 4)],
    }));

    // ── Shooting Stars ─────────────────────────────────────────────────────
    class ShootingStar {
      constructor() { this.reset(); }
      reset() {
        this.x = Math.random() * W * 1.2 - W * 0.1;
        this.y = Math.random() * H * 0.5;
        this.len = Math.random() * 180 + 80;
        this.speed = Math.random() * 14 + 8;
        this.angle = (Math.PI / 4) + (Math.random() - 0.5) * 0.3;
        this.alpha = 0;
        this.state = 'fadein'; // fadein | travel | fadeout
        this.traveled = 0;
        this.totalDist = Math.random() * 400 + 200;
        this.width = Math.random() * 1.5 + 0.5;
        this.hue = Math.random() > 0.5 ? '255,255,255' : '147,197,253';
      }
      update() {
        const dx = Math.cos(this.angle) * this.speed;
        const dy = Math.sin(this.angle) * this.speed;
        this.x += dx; this.y += dy;
        this.traveled += this.speed;
        if (this.state === 'fadein') {
          this.alpha += 0.06;
          if (this.alpha >= 1) { this.alpha = 1; this.state = 'travel'; }
        } else if (this.state === 'travel') {
          if (this.traveled > this.totalDist * 0.7) this.state = 'fadeout';
        } else {
          this.alpha -= 0.04;
          if (this.alpha <= 0) this.reset();
        }
      }
      draw(ctx) {
        const tx = this.x - Math.cos(this.angle) * this.len;
        const ty = this.y - Math.sin(this.angle) * this.len;
        const grad = ctx.createLinearGradient(tx, ty, this.x, this.y);
        grad.addColorStop(0, `rgba(${this.hue},0)`);
        grad.addColorStop(0.7, `rgba(${this.hue},${this.alpha * 0.3})`);
        grad.addColorStop(1, `rgba(${this.hue},${this.alpha})`);
        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(this.x, this.y);
        ctx.strokeStyle = grad;
        ctx.lineWidth = this.width;
        ctx.stroke();
        // bright tip
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.width * 1.2, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${this.hue},${this.alpha})`;
        ctx.fill();
      }
    }

    // Stagger shooting star spawns
    const shootingStars = Array.from({ length: 6 }, (_, i) => {
      const s = new ShootingStar();
      s.traveled = (s.totalDist / 6) * i; // offset so they don't all appear at once
      return s;
    });

    // ── Nebula Particles ───────────────────────────────────────────────────
    const NEBULA_COUNT = 40;
    const nebulas = Array.from({ length: NEBULA_COUNT }, () => ({
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 120 + 40,
      alpha: Math.random() * 0.04 + 0.01,
      color: ['79,142,247', '124,58,237', '245,158,11', '16,185,129'][Math.floor(Math.random() * 4)],
      vx: (Math.random() - 0.5) * 0.04,
      vy: (Math.random() - 0.5) * 0.04,
    }));

    let frame = 0;
    let animId;

    function draw() {
      ctx.clearRect(0, 0, W, H);

      // Nebula clouds
      nebulas.forEach(n => {
        n.x += n.vx; n.y += n.vy;
        if (n.x < -n.r) n.x = W + n.r;
        if (n.x > W + n.r) n.x = -n.r;
        if (n.y < -n.r) n.y = H + n.r;
        if (n.y > H + n.r) n.y = -n.r;
        const g = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r);
        g.addColorStop(0, `rgba(${n.color},${n.alpha})`);
        g.addColorStop(1, `rgba(${n.color},0)`);
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fillStyle = g;
        ctx.fill();
      });

      // Stars with twinkling
      stars.forEach(s => {
        const twinkle = Math.sin(frame * s.speed + s.phase);
        const a = s.alpha * (0.6 + 0.4 * twinkle);
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fillStyle = s.color.replace(')', `,${a})`).replace('rgb', 'rgba').replace('#', '');
        // For hex colors use a simpler approach
        ctx.globalAlpha = a;
        ctx.fillStyle = s.color;
        ctx.fill();
        ctx.globalAlpha = 1;

        // Occasional star glow
        if (s.r > 1 && a > 0.7) {
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.r * 3, 0, Math.PI * 2);
          const glow = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, s.r * 3);
          glow.addColorStop(0, `rgba(255,255,255,${a * 0.15})`);
          glow.addColorStop(1, 'rgba(255,255,255,0)');
          ctx.fillStyle = glow;
          ctx.fill();
        }
      });

      // Shooting stars
      shootingStars.forEach(s => { s.update(); s.draw(ctx); });

      frame++;
      animId = requestAnimationFrame(draw);
    }

    draw();

    const onResize = () => {
      W = window.innerWidth; H = window.innerHeight;
      canvas.width = W; canvas.height = H;
      stars.forEach(s => { s.x = Math.random() * W; s.y = Math.random() * H; });
      nebulas.forEach(n => { n.x = Math.random() * W; n.y = Math.random() * H; });
    };
    window.addEventListener('resize', onResize);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', onResize);
    };
  }, []);

  return <canvas ref={canvasRef} id="starfield-canvas" style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 0 }} />;
}
