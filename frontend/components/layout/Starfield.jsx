'use client';
import{useEffect,useRef}from'react';
export function Starfield(){
  const ref=useRef(null);
  useEffect(()=>{
    const canvas=ref.current;if(!canvas)return;
    const ctx=canvas.getContext('2d');
    let W=window.innerWidth,H=window.innerHeight;
    canvas.width=W;canvas.height=H;
    const COLS=['#ffffff','#93c5fd','#c4b5fd','#fbbf24','#a5f3fc'];
    const stars=Array.from({length:260},()=>({x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.5+0.2,alpha:Math.random()*0.8+0.15,speed:Math.random()*0.015+0.003,phase:Math.random()*Math.PI*2,color:COLS[Math.floor(Math.random()*COLS.length)]}));
    const NEB=['79,142,247','124,58,237','245,158,11','16,185,129','20,184,166'];
    const nebulas=Array.from({length:30},()=>({x:Math.random()*W,y:Math.random()*H,r:Math.random()*140+50,alpha:Math.random()*0.045+0.008,color:NEB[Math.floor(Math.random()*NEB.length)],vx:(Math.random()-.5)*.035,vy:(Math.random()-.5)*.035}));
    class Shooter{constructor(d=0){this.delay=d;this.active=d===0;this.waited=0;this.reset();}reset(){this.x=Math.random()*W*1.3-W*.15;this.y=Math.random()*H*.55;this.len=Math.random()*200+80;this.spd=Math.random()*16+9;this.ang=Math.PI/4+(Math.random()-.5)*.35;this.alpha=0;this.state='in';this.dist=0;this.total=Math.random()*450+180;this.w=Math.random()*1.8+.4;this.hue=Math.random()>.4?'255,255,255':'147,197,253';this.cooldown=Math.random()*400+150;this.waited=0;}update(){if(!this.active){this.waited++;if(this.waited>=this.delay)this.active=true;return;}if(this.state==='wait'){this.waited++;if(this.waited>=this.cooldown){this.waited=0;this.reset();this.active=true;this.state='in';}return;}this.x+=Math.cos(this.ang)*this.spd;this.y+=Math.sin(this.ang)*this.spd;this.dist+=this.spd;if(this.state==='in'){this.alpha=Math.min(1,this.alpha+.07);if(this.alpha>=1)this.state='go';}if(this.state==='go'&&this.dist>this.total*.65)this.state='out';if(this.state==='out'){this.alpha=Math.max(0,this.alpha-.05);if(this.alpha<=0){this.waited=0;this.state='wait';}}}draw(ctx){if(!this.active||this.state==='wait')return;const tx=this.x-Math.cos(this.ang)*this.len,ty=this.y-Math.sin(this.ang)*this.len;const g=ctx.createLinearGradient(tx,ty,this.x,this.y);g.addColorStop(0,`rgba(${this.hue},0)`);g.addColorStop(.65,`rgba(${this.hue},${this.alpha*.28})`);g.addColorStop(1,`rgba(${this.hue},${this.alpha})`);ctx.beginPath();ctx.moveTo(tx,ty);ctx.lineTo(this.x,this.y);ctx.strokeStyle=g;ctx.lineWidth=this.w;ctx.stroke();ctx.beginPath();ctx.arc(this.x,this.y,this.w*1.4,0,Math.PI*2);ctx.fillStyle=`rgba(${this.hue},${this.alpha})`;ctx.fill();}}
    const shooters=Array.from({length:7},(_,i)=>new Shooter(i*55));
    let frame=0,animId;
    const draw=()=>{
      ctx.clearRect(0,0,W,H);
      nebulas.forEach(n=>{n.x+=n.vx;n.y+=n.vy;if(n.x<-n.r)n.x=W+n.r;if(n.x>W+n.r)n.x=-n.r;if(n.y<-n.r)n.y=H+n.r;if(n.y>H+n.r)n.y=-n.r;const g=ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,n.r);g.addColorStop(0,`rgba(${n.color},${n.alpha})`);g.addColorStop(1,`rgba(${n.color},0)`);ctx.beginPath();ctx.arc(n.x,n.y,n.r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();});
      stars.forEach(s=>{const tw=.6+.4*Math.sin(frame*s.speed+s.phase);const a=s.alpha*tw;ctx.globalAlpha=a;ctx.fillStyle=s.color;ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();if(s.r>1&&a>.6){const glow=ctx.createRadialGradient(s.x,s.y,0,s.x,s.y,s.r*3.5);glow.addColorStop(0,`rgba(255,255,255,${a*.18})`);glow.addColorStop(1,'rgba(255,255,255,0)');ctx.beginPath();ctx.arc(s.x,s.y,s.r*3.5,0,Math.PI*2);ctx.fillStyle=glow;ctx.fill();}ctx.globalAlpha=1;});
      shooters.forEach(s=>{s.update();s.draw(ctx);});
      frame++;animId=requestAnimationFrame(draw);
    };
    draw();
    const onResize=()=>{W=window.innerWidth;H=window.innerHeight;canvas.width=W;canvas.height=H;stars.forEach(s=>{s.x=Math.random()*W;s.y=Math.random()*H;});nebulas.forEach(n=>{n.x=Math.random()*W;n.y=Math.random()*H;});};
    window.addEventListener('resize',onResize);
    return()=>{cancelAnimationFrame(animId);window.removeEventListener('resize',onResize);};
  },[]);
  return <canvas ref={ref} id="starfield-canvas"/>;
}
