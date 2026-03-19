(function () {
  "use strict";

  var TOGGLE_DEFS = {
    "/hideclothes":   [{ id: "Param47", value: 1.0 }],
    "/hideunderwear": [{ id: "Param47", value: 1.0 }, { id: "Param81", value: 1.0 }],
    "/hidebody":      [{ id: "Param79", value: 1.0 }],
    "/hidehead":      [{ id: "Param80", value: 1.0 }],
    "/shorthair":     [{ id: "Param18", value: 1.0 }],
    "/hidecover":     [{ id: "Param82", value: 1.0 }],
  };

  var TIMED_DEFS = {
    "/tongue": { params: [{ id: "Param60", value: 1.0 }, { id: "ParamMouthOpenY", value: 0.8 }], duration: 1200 },
  };

  var activeToggles = new Set();
  var activeTimers = {};
  var _managedParams = new Set();
  var _cubism = null;
  var _core = null;
  var _savedBuf = null;

  function ensureModel() {
    if (_core && _savedBuf) return true;
    try {
      var mgr = window._L2DM && window._L2DM.getInstance();
      if (!mgr) return false;
      var app = mgr.getModel(0);
      if (!app || !app._model) return false;

      _cubism = app._model;
      _core = _cubism._model;
      if (!_core || !_core.parameters || !_core.parameters.ids) {
        _core = null;
        return false;
      }

      var sp = _cubism._savedParameters;
      if (sp) {
        if (sp._ptr && typeof sp._ptr.length === "number") _savedBuf = sp._ptr;
        else if (typeof sp.length === "number") _savedBuf = sp;
        else if (sp._v && typeof sp._v.length === "number") _savedBuf = sp._v;
      }

      console.log("[Live2D Toggle] Model ready —", _core.parameters.ids.length, "params");
      return true;
    } catch (e) {
      return false;
    }
  }

  function computeOverrides() {
    var overrides = {};
    activeToggles.forEach(function (cmd) {
      var params = TOGGLE_DEFS[cmd];
      if (params) {
        for (var i = 0; i < params.length; i++) {
          overrides[params[i].id] = params[i].value;
        }
      }
    });
    for (var cmd in activeTimers) {
      var def = TIMED_DEFS[cmd];
      if (def) {
        for (var i = 0; i < def.params.length; i++) {
          overrides[def.params[i].id] = def.params[i].value;
        }
      }
    }
    return overrides;
  }

  function setParam(idx, value) {
    _core.parameters.values[idx] = value;
    if (_savedBuf) _savedBuf[idx] = value;
  }

  (function tick() {
    if ((_managedParams.size > 0 || activeToggles.size > 0 || Object.keys(activeTimers).length > 0) && (_core || ensureModel()) && _core) {
      var overrides = computeOverrides();
      var ids = _core.parameters.ids;

      for (var paramId in overrides) {
        var idx = ids.indexOf(paramId);
        if (idx !== -1) setParam(idx, overrides[paramId]);
        _managedParams.add(paramId);
      }

      _managedParams.forEach(function (paramId) {
        if (!(paramId in overrides)) {
          var idx = ids.indexOf(paramId);
          if (idx !== -1) setParam(idx, 0.0);
          _managedParams.delete(paramId);
        }
      });
    }
    requestAnimationFrame(tick);
  })();

  function handleToggle(command) {
    if (command === "/reset") {
      activeToggles.clear();
      for (var t in activeTimers) { clearTimeout(activeTimers[t]); }
      activeTimers = {};
      console.log("[Live2D Toggle] All toggles cleared");
      return;
    }

    if (command in TIMED_DEFS) {
      if (activeTimers[command]) {
        clearTimeout(activeTimers[command]);
        delete activeTimers[command];
        console.log("[Live2D Toggle] " + command + " cancelled");
      } else {
        if (!_core) ensureModel();
        activeTimers[command] = setTimeout(function () {
          delete activeTimers[command];
          console.log("[Live2D Toggle] " + command + " expired");
        }, TIMED_DEFS[command].duration);
        console.log("[Live2D Toggle] " + command + " → ON (" + TIMED_DEFS[command].duration + "ms)");
      }
      return;
    }

    if (!(command in TOGGLE_DEFS)) return;

    if (activeToggles.has(command)) {
      activeToggles.delete(command);
      console.log("[Live2D Toggle] " + command + " → OFF");
    } else {
      activeToggles.add(command);
      console.log("[Live2D Toggle] " + command + " → ON");
    }
    if (!_core) ensureModel();
  }

  window._live2dToggles = {
    active: function () { return Array.from(activeToggles); },
    timers: function () { return Object.keys(activeTimers); },
    clear: function () { activeToggles.clear(); for (var t in activeTimers) { clearTimeout(activeTimers[t]); } activeTimers = {}; },
    defs: TOGGLE_DEFS,
    diag: function () {
      ensureModel();
      if (_core) {
        var ids = _core.parameters.ids;
        var vals = _core.parameters.values;
        ["Param47", "Param81", "Param79", "Param80", "Param18", "Param82", "Param60"].forEach(function (p) {
          var i = ids.indexOf(p);
          console.log(p, "→ idx:", i, "live:", i >= 0 ? vals[i] : "N/A", "saved:", i >= 0 && _savedBuf ? _savedBuf[i] : "N/A");
        });
      }
    },
  };

  var _OrigWS = window.WebSocket;
  window.WebSocket = new Proxy(_OrigWS, {
    construct: function (target, args) {
      var ws = args.length > 1 ? new target(args[0], args[1]) : new target(args[0]);
      ws.addEventListener("message", function (e) {
        try {
          var msg = JSON.parse(e.data);
          if (msg.type === "toggle-parameter" && msg.command) {
            handleToggle(msg.command);
          }
        } catch (_) {}
      });
      return ws;
    },
  });

  console.log("[Live2D Toggle] Persistent toggle system loaded");
})();
