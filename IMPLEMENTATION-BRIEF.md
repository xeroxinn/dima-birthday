# Dima's Workday Game — Implementation Brief

## Target File
`/Users/igorraev/Work/Development/.tmp/dima-birthday/game/index.html`

Single self-contained HTML file (~1340 lines). Canvas-based pixel-art game with embedded CSS and JS. Russian language. No external dependencies except Google Font (Press Start 2P).

---

## Architecture Overview

**Rendering**: `<canvas>` element, `requestAnimationFrame` game loop. Pixel art drawn with `px(ctx,x,y,s,color)` helper. `ps` = pixel size (responsive).

**State**: Global object `S` holds all game state (progress, combo, flags for one-time events, etc.)

**Entities**: Global `ents` object: `{bugs:[], teas:[], particles:[], wife:null, dogs:[], marshrutka:null}`

**Events**: `checkEvents()` runs every frame, checks `S.progress` thresholds, triggers events via `setTimeout`. Each event has a boolean flag in `S` (e.g., `S.crashShown`) to fire only once.

**Sound**: Web Audio API. `tone(freq, duration, type, volume)` helper. Named functions like `sfxClick()`, `sfxTea()`, `sfxSquash()`, etc.

**Popups**: Choice popups are DOM elements created dynamically, appended to `document.body`, removed on button click.

**Existing events timeline**: ~20% fake crash, ~30% dogs, ~40% khachapuri choice, ~55% marshrutka, ~65% swimming minigame, ~78% chacha choice, ~85% boss bug.

---

## Feature 1: Wife Click → Kiss Sound + Hearts

### Current wife behavior (lines ~682-697, ~1247-1251)
Wife entity spawns from right edge, walks left (`vx: -1.5`), stops at `cW * 0.6` (phase 0→1), waits 60 frames (phase 1), then walks back left and delivers tea (phase 1→2). No click interaction exists.

### What to add
1. **New sound** `sfxKiss()` — two warm sine tones, e.g. `tone(520, 0.15, 'sine', 0.06)` then `tone(660, 0.2, 'sine', 0.05)` after 100ms.

2. **Click detection in `handleGameClick()`** (line ~1076) — add wife hit detection BEFORE the code click section. Check if `ents.wife` exists, is not done, and click coordinates are within ~30px of her position (`ents.wife.x`, `ents.wife.y * ps`). When hit:
   - Play `sfxKiss()`
   - Call `spawnHearts(wifeScreenX, wifeScreenY)` (new function)
   - Show float text `"💋 +Love!"` in pink
   - Brief pink screen flash

3. **New function `spawnHearts(x, y)`** — spawn 6-8 particles that float UPWARD (negative vy: -2 to -4, small random vx), larger size (4-6px), pink/red color base `'rgba(255,107,157,'`. Use the existing particle system (`ents.particles`).

---

## Feature 2: More Interactions & Pop-ups

Add these to `checkEvents()` with new flags in `S`. Follow the exact same pattern as existing events (flag check → `setTimeout` → popup function).

### 2a. Cat on Keyboard (~15%)
- **Flag**: `S.catShown`
- **Trigger**: `S.progress >= 15`
- **Behavior**: Spawn a cat entity that walks across the screen (like dogs, but a cat sprite). When it reaches the desk area, -2% progress, flavor text "Кот прошёл по клавиатуре! 🐱 -2% к коду"
- **Pixel art** `drawCat(ctx, ox, oy, s, frame)`: Small cat — body in `#555`/`#666`, pointed ears, tail that sways with frame. ~6x4 pixels.
- Add `ents.cat` (single entity, similar to marshrutka pattern — null when inactive)

### 2b. Mom Calls (~35%)
- **Flag**: `S.momCallShown`
- **Popup** (DOM, same pattern as chacha/khachapuri):
  ```
  📱 МАМА ЗВОНИТ!
  "Сынок, ты кушал?"
  [Ответить] [Сбросить]
  ```
- **"Ответить"**: Flavor text "Мама довольна. +1% к карме", `S.progress += 1`
- **"Сбросить"**: Flavor text "Мама перезвонит... через 5 минут. 😬", no penalty
- **Sound**: New `sfxPhone()` — short repeating tone like a ringtone

### 2c. Stack Overflow Down (~50%)
- **Flag**: `S.soDownShown`
- **Behavior**: Show a panic overlay (DOM element, full-screen semi-transparent):
  ```
  ⚠️ STACK OVERFLOW УПАЛ!
  Код писать невозможно...
  ```
- Set `S.soDown = true` for 3 seconds — during this time, code clicks in `handleGameClick` do nothing (add early return check)
- After 3s: remove overlay, set `S.soDown = false`, flavor text "Stack Overflow вернулся! Фух..."
- **Sound**: `sfxBoss()` (reuse existing alarm sound)

### 2d. Pizza Delivery (~60%)
- **Flag**: `S.pizzaShown`
- **Popup** (DOM, same as khachapuri):
  ```
  🍕 ПИЦЦА!
  Курьер принёс маргариту. Съесть?
  [Ещё бы!] [Диета...]
  ```
- **"Ещё бы!"**: +2% progress, flavor text "Пицца... 🍕 Энергия восстановлена!"
- **"Диета..."**: 2x multiplier for 4s, flavor text "Сила воли +100. Пицца ждёт в холодильнике."
- **Pixel art** `drawPizza(ctx, ox, oy, s)`: Triangle slice, ~5x4 pixels, yellow cheese + red sauce

### 2e. Deadline Email (~92%)
- **Flag**: `S.deadlineShown`
- **Behavior**: Show scary popup:
  ```
  📧 НОВОЕ ПИСЬМО
  От: Boss
  Тема: DEADLINE СЕГОДНЯ!!!
  "Игра должна быть готова к 22:00.
  Без вариантов."
  [ПАНИКА!]
  ```
- On dismiss: Set `S.mult = 3` for 8 seconds (panic mode), flavor text "ПАНИКА! x3 к скорости кодинга!", screen shake, red flash
- **Sound**: `sfxBoss()` reuse

### CSS for new popups
Reuse existing popup styles (`.chacha-popup` / `.khacha-popup` pattern). Create `.mom-popup`, `.pizza-popup`, `.deadline-popup` with appropriate accent colors (mom = green, pizza = orange, deadline = red).

---

## Feature 3: Better Background

### Current (line ~585-591)
```js
ctx.fillStyle='#0f0e17';
ctx.fillRect(0,0,cW,cH);
// Grid
ctx.strokeStyle='rgba(255,255,255,.015)';
```

### Replace with time-of-day gradient
In `gameLoop()` / `renderNormalPhase()`, replace the flat fill with a vertical gradient based on `S.gameTime` (value in minutes, starts at 360 = 06:00, ends at 1320 = 22:00):

```js
function getTimeColors(gameTime) {
  // gameTime in minutes: 360=6:00, 720=12:00, 1080=18:00, 1320=22:00
  const t = (gameTime - 360) / (1320 - 360); // 0..1
  if (t < 0.15)      return { top: '#1a1a3e', bot: '#2a1a4e', star: 0.6 };  // early morning
  if (t < 0.3)       return { top: '#2a3a6e', bot: '#4a3a5e', star: 0.2 };  // morning
  if (t < 0.5)       return { top: '#3a5a8e', bot: '#4a4a6e', star: 0.0 };  // midday
  if (t < 0.7)       return { top: '#5a4a6e', bot: '#6a3a4e', star: 0.1 };  // afternoon
  if (t < 0.85)      return { top: '#4a2a4e', bot: '#3a1a3e', star: 0.4 };  // sunset
  return                     { top: '#0f0e17', bot: '#1a1a2e', star: 0.8 };  // night
}
```

Draw as canvas gradient:
```js
const colors = getTimeColors(S.gameTime);
const grad = ctx.createLinearGradient(0, 0, 0, cH);
grad.addColorStop(0, colors.top);
grad.addColorStop(1, colors.bot);
ctx.fillStyle = grad;
ctx.fillRect(0, 0, cW, cH);
```

### Tbilisi skyline
Draw a simple dark silhouette at bottom of canvas. Array of building heights:
```js
const SKYLINE = [3,5,4,8,6,3,10,7,4,5,12,8,5,3,6,9,4,7,5,3];
```
Draw as filled rectangles in dark color slightly lighter than background. Church dome shape for one building (Tbilisi vibe). Render in `renderNormalPhase()` after background, before entities.

### Canvas stars (replace CSS stars)
Remove the CSS `.stars` div and its initialization code (lines ~1294-1302). Instead, create an array of star objects at init:
```js
const stars = Array.from({length: 80}, () => ({
  x: Math.random() * cW, y: Math.random() * cH * 0.6,
  size: 1 + Math.random(), phase: Math.random() * Math.PI * 2
}));
```
Render in game loop with twinkling alpha based on `sin(frame * 0.02 + star.phase)`. Multiply alpha by `colors.star` from time-of-day so stars fade during daytime.

### Shooting stars
Every ~1800 frames (~30s), spawn a shooting star: a bright dot that moves diagonally across the upper portion of the screen with a fading trail. Simple: push to a `shootingStars` array, render as a line with decreasing alpha.

### Ambient code symbols
Array of ~15 floating symbols (`{ }`, `< >`, `//`, `=>`, `fn`, `if`, `0x`). Very faint (`alpha: 0.04-0.08`), slowly drift upward (`vy: -0.2`), wrap around when off top. Render with `ctx.font` and `ctx.fillText`. Reset y to `cH + 20` when `y < -20`.

---

## Feature 4: Caffeine State

### New state in `S`
```js
S.totalTeaCollected = 0
S.caffeineActive = false
S.caffeineEnd = 0
```

### Trigger
In the tea collection handler (line ~1124-1131), after `S.tea++`:
```js
S.totalTeaCollected++;
if (S.totalTeaCollected % 5 === 0) activateCaffeine();
```

### `activateCaffeine()` function
```js
function activateCaffeine() {
  S.caffeineActive = true;
  S.caffeineEnd = Date.now() + 12000;
  showFlavor("☕ КАФЕИН! Всё ускоряется!");
  sfxMilestone();
  // Visual: add CSS class
  document.getElementById('gameArea').classList.add('caffeine');
  // Speed up bugs
  clearInterval(bugInt);
  bugInt = setInterval(spawnBug, 800);
}
```

### Check expiry in game loop
At the start of `renderNormalPhase()`:
```js
if (S.caffeineActive && Date.now() > S.caffeineEnd) {
  S.caffeineActive = false;
  document.getElementById('gameArea').classList.remove('caffeine');
  // Restore normal bug rate
  clearInterval(bugInt);
  bugInt = setInterval(spawnBug, 1800);
  showFlavor("Кафеин прошёл... 😴");
}
```

### Effects during caffeine
- **Bug speed**: In `spawnBug()`, multiply `speedMult` by 2 if `S.caffeineActive`
- **Click bonus**: In `handleGameClick()` code click section, multiply `gain` by 1.5 if `S.caffeineActive`
- **Combo timer**: Use 800ms instead of 1500ms if `S.caffeineActive`

### CSS for caffeine visual
```css
.caffeine {
  animation: caffeineJitter 0.1s infinite;
  box-shadow: inset 0 0 60px rgba(0,255,136,0.15);
}
@keyframes caffeineJitter {
  0% { transform: translate(0, 0); }
  25% { transform: translate(1px, -1px); }
  50% { transform: translate(-1px, 1px); }
  75% { transform: translate(1px, 1px); }
  100% { transform: translate(-1px, -1px); }
}
```

### Caffeine HUD indicator
Reuse the boost indicator pattern (`.boost-ind`). Add a new element:
```html
<div class="caffeine-ind" id="caffeineInd">☕ КАФЕИН!</div>
```
Style it green, show/hide with `.active` class same as boost indicator.

---

## Feature 5: Reduce Tea Frequency

### Current (line 1316)
```js
teaInt=setInterval(spawnTea,5500);
```

### Change to
```js
teaInt=setInterval(spawnTea,9000);
```

During caffeine mode, temporarily set to 6000ms. Restore to 9000ms when caffeine ends.

---

## Feature 6: Gift Codes Copy-to-Clipboard

### Current victory screen (lines ~342-351)
Two `.gift` divs with `.gift-code` children (`#gc1`, `#gc2`). Currently display-only.

### CSS additions
```css
.gift {
  cursor: pointer;
  transition: border-color 0.3s, box-shadow 0.3s;
}
.gift:hover {
  border-color: var(--green);
  box-shadow: 0 0 12px rgba(0,255,136,0.3);
}
.gift.copied {
  border-color: var(--green);
}
.gift .copy-hint {
  font-size: clamp(5px, 1.2vw, 6px);
  color: var(--dim);
  margin-top: 4px;
}
.gift .copied-msg {
  font-size: clamp(6px, 1.5vw, 8px);
  color: var(--green);
  margin-top: 4px;
  display: none;
}
.gift.copied .copy-hint { display: none; }
.gift.copied .copied-msg { display: block; }
```

### HTML changes
Add hint text inside each `.gift` div:
```html
<div class="copy-hint">нажми чтобы скопировать</div>
<div class="copied-msg">✓ Скопировано!</div>
```

### JS — add in `winGame()` function, after victory screen is shown
```js
document.querySelectorAll('.gift').forEach(g => {
  g.addEventListener('click', () => {
    const code = g.querySelector('.gift-code').textContent;
    navigator.clipboard.writeText(code).then(() => {
      g.classList.add('copied');
      sfxTea(); // satisfying confirmation sound
      setTimeout(() => g.classList.remove('copied'), 2000);
    });
  });
});
```

---

## New State Flags Summary

Add to the `S` object (line ~521):
```js
catShown: false,
momCallShown: false,
soDownShown: false,
soDown: false,        // true while SO is "down" (blocks clicks)
pizzaShown: false,
deadlineShown: false,
totalTeaCollected: 0,
caffeineActive: false,
caffeineEnd: 0,
```

Add to `ents` (line ~536):
```js
cat: null,
```

---

## New Sound Effects Summary

```js
function sfxKiss() {
  tone(520, 0.15, 'sine', 0.06);
  setTimeout(() => tone(660, 0.2, 'sine', 0.05), 100);
}
function sfxPhone() {
  for(let i = 0; i < 4; i++) setTimeout(() => tone(800, 0.08, 'square', 0.04), i * 150);
}
```

---

## Updated Event Timeline

| % | Event | Type |
|---|-------|------|
| 15 | Cat on keyboard | New — sprite + flavor |
| 20 | Fake crash | Existing |
| 25 | Alpha milestone | Existing |
| 30 | Dogs | Existing |
| 35 | Mom calls | New — choice popup |
| 40 | Khachapuri | Existing |
| 50 | Stack Overflow down | New — 3s block overlay |
| 50 | Beta milestone | Existing |
| 55 | Marshrutka | Existing |
| 60 | Pizza delivery | New — choice popup |
| 65 | Swimming minigame | Existing |
| 78 | Chacha | Existing |
| 85 | Boss bug | Existing |
| 92 | Deadline email | New — panic boost |

---

## Testing Checklist
- [ ] Background gradient changes as game clock advances
- [ ] Stars twinkle, fade during daytime, visible at night
- [ ] Skyline visible at bottom of game area
- [ ] Shooting star appears occasionally
- [ ] Click wife → kiss sound + hearts float up
- [ ] Cat event at 15%, walks across screen, -2% progress
- [ ] Mom call popup at 35%, both choices work
- [ ] SO down overlay at 50%, blocks clicks for 3s
- [ ] Pizza popup at 60%, both choices work
- [ ] Deadline popup at 92%, gives 3x multiplier
- [ ] Tea spawns less frequently (every 9s vs 5.5s)
- [ ] Every 5th tea triggers caffeine mode
- [ ] Caffeine: screen jitters, bugs faster, clicks stronger
- [ ] Caffeine wears off after 12s
- [ ] Gift codes clickable on victory screen
- [ ] Clipboard copy works, "Скопировано!" feedback shows
- [ ] All existing events still trigger correctly
- [ ] Game completes to victory screen without errors
