(function(){
  // Nutrition Solutions AI Sales Coach – Intercom-style widget
  // Loads as a single embed (<script src="https://yourdomain.com/widget.js" defer></script>).
  // Uses Shadow DOM for full CSS isolation.

  var WIDGET_ID = 'ns-coach-widget';
  var SHADOW_HOST_ID = 'ns-coach-shadow-host';
  var API_BASE = (window.NSCoachConfig && window.NSCoachConfig.apiBase) || '/api';

  // Short-term memory (per session)
  var session = {
    id: null,
    stateId: null,
    profile: {},
    goal: null,
    habits: {},
    whyNow: '',
    offrouteCount: 0
  };

  // Utilities
  function uid(){ return 'ns_'+Math.random().toString(36).slice(2,9); }
  function delay(ms){ return new Promise(r=>setTimeout(r,ms)); }
  async function fetchText(url){ const r = await fetch(url,{cache:'no-cache'}); if(!r.ok) throw new Error('fetch '+url); return r.text(); }
  async function fetchJSON(url, opts){ const r = await fetch(url, Object.assign({headers:{'Content-Type':'application/json'}}, opts)); if(!r.ok) throw new Error('fetch '+url); return r.json(); }
  function chunkText(t, max){ const out=[]; let s=t.trim(); while(s.length>max){ let i=s.lastIndexOf(' ', max); if(i<0) i=max; out.push(s.slice(0,i)); s=s.slice(i).trim(); } if(s) out.push(s); return out; }
  function setTyping(shadow, on){ var el = shadow.getElementById('ns-typing'); if(!el) return; el.hidden = !on; }
  function scrollToBottom(shadow){ var pane = shadow.getElementById('ns-transcript'); if(pane) pane.scrollTop = pane.scrollHeight; }
  function setQuickReplies(shadow, chips){ var rail = shadow.getElementById('ns-quick'); rail.innerHTML=''; if(!chips||!chips.length){ rail.hidden=true; return; } rail.hidden=false; chips.forEach(function(label){ var b=document.createElement('button'); b.className='ns-chip'; b.textContent=label; b.addEventListener('click', function(){ emitUser(shadow, label); }); rail.appendChild(b); }); }

  // DOM helpers in Shadow DOM
  function addBubble(shadow, role, text){ var t = shadow.getElementById('ns-transcript'); var b = document.createElement('div'); b.className = 'ns-bubble '+role; b.textContent = text; t.appendChild(b); scrollToBottom(shadow); return b; }
  function addSystem(shadow, text){ var t = shadow.getElementById('ns-transcript'); var b=document.createElement('div'); b.className='ns-system'; b.textContent=text; t.appendChild(b); scrollToBottom(shadow); return b; }
  function addCarousel(shadow, items){ var t = shadow.getElementById('ns-transcript'); var wrap=document.createElement('div'); wrap.className='ns-carousel'; items.forEach(function(it){ var card=document.createElement('div'); card.className='ns-card';
      var img=document.createElement('img'); img.alt = (it.name||'Transformation'); img.src = it.image || '';
      var h4=document.createElement('h4'); h4.textContent = (it.name? it.name+' · ':'') + (it.age? it.age+' · ': '') + (it.goal||'');
      var p=document.createElement('p'); p.textContent = (it.time||'') + (it.quote? ' | "'+it.quote+'"':'' );
      var cta=document.createElement('button'); cta.className='ns-cta'; cta.textContent='I want results like this'; cta.addEventListener('click', function(){
        session.interest='carousel'; goTo('S8');
      });
      card.appendChild(img); card.appendChild(h4); card.appendChild(p); card.appendChild(cta); wrap.appendChild(card);
    });
    t.appendChild(wrap); scrollToBottom(shadow); return wrap;
  }

  // Message pacing for assistant
  async function say(shadow, text, opts){ opts = opts||{}; var parts = chunkText(text, 220); for (var i=0;i<parts.length;i++){ setTyping(shadow,true); await delay(400 + Math.random()*400 + (opts.afterWidget?300:0)); addBubble(shadow,'assistant', parts[i]); setTyping(shadow,false); }
  }

  // Conversation scripts
  var Scripts = { flow:null, offroute:null, rules:null };

  async function loadScripts(){
    // Allow host to override base path for static JSON
    var base = (window.NSCoachConfig && window.NSCoachConfig.assetsBase) || '/conversation';
    const [flow, offroute, rules] = await Promise.all([
      fetchJSON(base + '/flow.json'),
      fetchJSON(base + '/offroute.json'),
      fetchJSON(base + '/recommendation_rules.json')
    ]);
    Scripts.flow = flow; Scripts.offroute = offroute; Scripts.rules = rules;
  }

  function currentState(){
    if(!Scripts.flow) return null;
    var id = session.stateId || Scripts.flow.start;
    return Scripts.flow.states.find(function(s){ return s.id===id; });
  }

  function detectOffroute(text){
    var rules = Scripts.offroute && Scripts.offroute.triggers || [];
    text = (text||'').toLowerCase();
    for (var i=0;i<rules.length;i++){
      var r = rules[i];
      var re = new RegExp(r.pattern, 'i');
      if (re.test(text)) return r;
    }
    return null;
  }

  async function handleOffroute(shadow, trigger, text){
    session.offrouteCount++;
    // Ask backend Agents SDK for an answer, optionally RAG
    try{
      var payload = { sessionId: session.id, text:text, context:{ stateId: session.stateId, profile: session.profile } };
      var resp = await fetchJSON(API_BASE + '/message', { method:'POST', body: JSON.stringify(payload) });
      if(resp && resp.reply){ await say(shadow, resp.reply); }
    }catch(e){ await say(shadow, "I couldn’t pull that up—one sec while we try again."); }
    // Bridge back
    await say(shadow, "Sound fair if we finish your quick assessment so I can tailor this?");
    setQuickReplies(shadow, ["Finish assessment"]);
  }

  async function emitUser(shadow, text){
    setQuickReplies(shadow, []);
    addBubble(shadow,'user', text);

    // Off-route detection
    var trig = detectOffroute(text);
    if (trig){ return handleOffroute(shadow, trig, text); }

    var st = currentState();
    if(!st){ return; }

    // Collect per-state
    if (st.collect){
      Object.keys(st.collect).forEach(function(key){
        if (st.collect[key]==='free') session[key] = text;
      });
    }

    // Simple transitions
    if (st.next){ session.stateId = st.next; return renderState(shadow); }
  }

  async function goTo(id){ session.stateId = id; if (shadowRootRef) await renderState(shadowRootRef); }

  async function renderState(shadow){
    var st = currentState(); if(!st) return;

    // Save memory progressively
    if (st.memoryWrite){ try{ await fetchJSON(API_BASE + '/memory/store', {method:'POST', body: JSON.stringify({ sessionId: session.id, data: st.memoryWrite.reduce(function(acc,k){ acc[k]=session[k]; return acc; }, {}) })}); }catch(e){} }

    // Render assistant copy and quick replies
    if(Array.isArray(st.say)){
      for (var i=0;i<st.say.length;i++){ await say(shadow, st.say[i]); }
    } else if (typeof st.say === 'string'){ await say(shadow, st.say); }

    if (st.quickReplies && st.quickReplies.length){ setQuickReplies(shadow, st.quickReplies); }

    // Special behaviors by state
    if (st.id === 'S2'){
      // Expect demographics; show chips via quick replies already in flow
    }
    if (st.id === 'S7'){
      // Load and show Transformation Carousel
      try{
        var qs = new URLSearchParams({ goal: session.goal||'', age: session.profile && session.profile.age||'', habits: session.habits && session.habits.summary||'' });
        var items = await fetchJSON(API_BASE + '/carousel?'+qs.toString());
        addCarousel(shadow, items||[]);
      }catch(e){ addSystem(shadow, 'Carousel unavailable. Showing general results.'); }
    }
    if (st.id === 'S8'){
      // Ask backend for recommendation synthesis
      try{
        var rec = await fetchJSON(API_BASE + '/recommend', { method:'POST', body: JSON.stringify({ profile: session.profile, goal: session.goal, habits: session.habits, whyNow: session.whyNow })});
        if (rec && rec.summary){ await say(shadow, rec.summary); }
        if (rec && rec.plan){ await say(shadow, 'I recommend '+rec.plan+'—built for how you live.'); }
        await say(shadow, 'Want the details or ready to start?');
        setQuickReplies(shadow, ['See Plan Details','Start My Plan']);
      }catch(e){ await say(shadow, 'I’m having a moment. Let’s keep this simple.'); setQuickReplies(shadow, ['See Plan Details']); }
    }

    // Default input enabled
    shadow.getElementById('ns-input').disabled = false;
  }

  // Init Shadow DOM host
  var shadowRootRef = null;
  async function mount(){
    if (document.getElementById(SHADOW_HOST_ID)) return;
    var host = document.createElement('div'); host.id = SHADOW_HOST_ID; document.body.appendChild(host);
    var shadow = host.attachShadow({mode:'open'});
    shadowRootRef = shadow;

    // Load template and CSS
    var [html, css] = await Promise.all([
      fetchText('/widget/chat-window.html'),
      fetchText('/widget/widget.css')
    ]);
    var tpl = document.createElement('template'); tpl.innerHTML = html; shadow.appendChild(tpl.content.cloneNode(true));
    var style = document.createElement('style'); style.textContent = css; shadow.appendChild(style);

    // Wire UI
    var bubble = shadow.getElementById('ns-bubble');
    var win = shadow.getElementById('ns-window');
    var close = shadow.getElementById('ns-close');
    var send = shadow.getElementById('ns-send');
    var input = shadow.getElementById('ns-input');

    function open(){ win.hidden=false; bubble.setAttribute('hidden',''); document.body.setAttribute('bubble-hidden',''); input.focus(); }
    function closeWin(){ win.hidden=true; bubble.removeAttribute('hidden'); document.body.removeAttribute('bubble-hidden'); }

    bubble.addEventListener('click', open);
    close.addEventListener('click', closeWin);

    function onSend(){ var text = input.value.trim(); if(!text) return; input.value=''; emitUser(shadow, text); }
    send.addEventListener('click', onSend);
    input.addEventListener('keydown', function(e){ if (e.key==='Enter' && !e.shiftKey){ e.preventDefault(); onSend(); }});

    window.NSCoachWidget = { open:open, close:closeWin };

    // Start session
    session.id = uid();
    try{
      await loadScripts();
      // Attempt to greet returning user
      try{
        var mem = await fetchJSON(API_BASE + '/memory/fetch', { method:'POST', body: JSON.stringify({ sessionId: session.id })});
        if (mem && mem.profile && mem.profile.name){ await say(shadow, 'Welcome back, '+mem.profile.name+'. Pick up where we left off?'); setQuickReplies(shadow, ['Resume','Start over']); }
      }catch(_){ }
      // Start flow
      session.stateId = Scripts.flow && Scripts.flow.start || 'S1';
      await renderState(shadow);
    }catch(e){ addSystem(shadow, 'Widget failed to initialize.'); }
  }

  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', mount); } else { mount(); }
})();
