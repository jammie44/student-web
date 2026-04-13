'use client';
const TK='sh_token',UK='sh_user',EK='sh_expiry',WEEK=7*24*60*60*1000;
export const saveAuth=(token,user)=>{if(typeof window==='undefined')return;localStorage.setItem(TK,token);localStorage.setItem(UK,JSON.stringify(user));localStorage.setItem(EK,String(Date.now()+WEEK));};
export const clearAuth=()=>{if(typeof window==='undefined')return;[TK,UK,EK].forEach(k=>localStorage.removeItem(k));};
export const getToken=()=>{if(typeof window==='undefined')return null;const t=localStorage.getItem(TK);if(!t)return null;const e=localStorage.getItem(EK);if(e&&Date.now()>parseInt(e)){clearAuth();return null;}return t;};
export const getStoredUser=()=>{if(typeof window==='undefined')return null;try{const u=localStorage.getItem(UK);return u?JSON.parse(u):null;}catch{return null;}};
export const refreshExpiry=()=>{if(typeof window==='undefined')return;if(localStorage.getItem(TK))localStorage.setItem(EK,String(Date.now()+WEEK));};
