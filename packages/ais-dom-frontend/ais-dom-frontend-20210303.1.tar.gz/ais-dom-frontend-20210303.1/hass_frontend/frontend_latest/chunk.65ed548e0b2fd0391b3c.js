(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[8237],{85415:(e,t,r)=>{"use strict";r.d(t,{q:()=>n,w:()=>i});const n=(e,t)=>e<t?-1:e>t?1:0,i=(e,t)=>n(e.toLowerCase(),t.toLowerCase())},81582:(e,t,r)=>{"use strict";r.d(t,{pB:()=>n});const n=e=>e.callApi("GET","config/config_entries/entry")},73728:(e,t,r)=>{"use strict";r.d(t,{Ky:()=>s,D4:()=>l,XO:()=>c,oi:()=>d,d4:()=>p,D7:()=>f,ZJ:()=>u,V3:()=>m,WW:()=>g});var n=r(95282),i=r(38346),o=r(5986);const a={"HA-Frontend-Base":`${location.protocol}//${location.host}`},s=(e,t)=>{var r;return e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(null===(r=e.userData)||void 0===r?void 0:r.showAdvanced)},a)},l=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`,void 0,a),c=(e,t,r)=>e.callApi("POST",`config/config_entries/flow/${t}`,r,a),d=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),p=e=>e.callApi("GET","config/config_entries/flow_handlers"),f=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),h=(e,t)=>e.subscribeEvents((0,i.D)((()=>f(e).then((e=>t.setState(e,!0)))),500,!0),"config_entry_discovered"),u=e=>(0,n._)(e,"_configFlowProgress",f,h),m=(e,t)=>u(e.connection).subscribe(t),g=(e,t)=>{const r=t.context.title_placeholders||{},n=Object.keys(r);if(0===n.length)return(0,o.Lh)(e,t.handler);const i=[];return n.forEach((e=>{i.push(e),i.push(r[e])})),e(`component.${t.handler}.config.flow_title`,...i)}},5986:(e,t,r)=>{"use strict";r.d(t,{Lh:()=>n});const n=(e,t)=>e(`component.${t}.title`)||t},2852:(e,t,r)=>{"use strict";r.d(t,{q:()=>c,t:()=>d});var n=r(15652),i=r(85415),o=r(91177),a=r(73728),s=r(5986),l=r(52871);const c=l.G,d=(e,t)=>(0,l.w)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:async e=>{const[t]=await Promise.all([(0,a.d4)(e),e.loadBackendTranslation("title",void 0,!0)]);return t.sort(((t,r)=>(0,i.w)((0,s.Lh)(e.localize,t),(0,s.Lh)(e.localize,r))))},createFlow:async(e,t)=>{const[r]=await Promise.all([(0,a.Ky)(e,t),e.loadBackendTranslation("config",t)]);return r},fetchFlow:async(e,t)=>{const r=await(0,a.D4)(e,t);return await e.loadBackendTranslation("config",r.handler),r},handleFlowStep:a.XO,deleteFlow:a.oi,renderAbortDescription(e,t){const r=(0,o.I)(e.localize,`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return r?n.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormStepDescription(e,t){const r=(0,o.I)(e.localize,`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return r?n.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,t,r)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.data.${r.name}`),renderShowFormStepFieldError:(e,t,r)=>e.localize(`component.${t.handler}.config.error.${r}`),renderExternalStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site"),renderExternalStepDescription(e,t){const r=(0,o.I)(e.localize,`component.${t.handler}.config.${t.step_id}.description`,t.description_placeholders);return n.dy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${r?n.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${r}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const r=(0,o.I)(e.localize,`component.${t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return n.dy`
        ${r?n.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${r}
              ></ha-markdown>
            `:""}
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.created_config","name",t.title)}
        </p>
      `},renderShowFormProgressHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormProgressDescription(e,t){const r=(0,o.I)(e.localize,`component.${t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return r?n.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""}})},52871:(e,t,r)=>{"use strict";r.d(t,{G:()=>i,w:()=>o});var n=r(47181);const i=()=>Promise.all([r.e(5009),r.e(8161),r.e(2955),r.e(8200),r.e(879),r.e(9543),r.e(2762),r.e(8374),r.e(5829),r.e(1480),r.e(4421),r.e(8101),r.e(8331),r.e(4940),r.e(4482)]).then(r.bind(r,27234)),o=(e,t,r)=>{(0,n.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:i,dialogParams:{...t,flowConfig:r}})}},38237:(e,t,r)=>{"use strict";r.r(t);r(53918);var n=r(15652),i=r(47181),o=r(85415),a=r(81582),s=r(73728),l=r(5986),c=r(2852);r(41725),r(84912);function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,i[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&n.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return y(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?y(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=g(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:m(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=m(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function p(e){var t,r=g(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function f(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function g(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function v(e,t,r){return(v="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=w(e)););return e}(e,t);if(n){var i=Object.getOwnPropertyDescriptor(n,t);return i.get?i.get.call(r):i.value}})(e,t,r||e)}function w(e){return(w=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const b=new Set(["met","rpi_power"]);!function(e,t,r,n){var i=d();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(u(o.descriptor)||u(i.descriptor)){if(h(o)||h(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(h(o)){if(h(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}f(o,i)}else t.push(o)}return t}(a.d.map(p)),e);i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,n.Mo)("onboarding-integrations")],(function(e,t){class d extends t{constructor(...t){super(...t),e(this)}}return{F:d,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"onboardingLocalize",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_entries",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_discovered",value:void 0},{kind:"field",key:"_unsubEvents",value:void 0},{kind:"method",key:"connectedCallback",value:function(){v(w(d.prototype),"connectedCallback",this).call(this),this.hass.loadBackendTranslation("title",void 0,!0),this._unsubEvents=(0,s.V3)(this.hass,(e=>{this._discovered=e;for(const t of e)t.context.title_placeholders&&this.hass.loadBackendTranslation("config",t.handler)}))}},{kind:"method",key:"disconnectedCallback",value:function(){v(w(d.prototype),"disconnectedCallback",this).call(this),this._unsubEvents&&(this._unsubEvents(),this._unsubEvents=void 0)}},{kind:"method",key:"render",value:function(){if(!this._entries||!this._discovered)return n.dy``;const e=[...this._entries.map((e=>{const t=(0,l.Lh)(this.hass.localize,e.domain);return[t,n.dy`
            <integration-badge
              .domain=${e.domain}
              .title=${t}
              badgeIcon="hass:check"
            ></integration-badge>
          `]})),...this._discovered.map((e=>{const t=(0,s.WW)(this.hass.localize,e);return[t,n.dy`
            <button .flowId=${e.flow_id} @click=${this._continueFlow}>
              <integration-badge
                clickable
                .domain=${e.handler}
                .title=${t}
              ></integration-badge>
            </button>
          `]}))].sort(((e,t)=>(0,o.q)(e[0],t[0]))).map((e=>e[1]));return n.dy`
      <p>
        ${this.onboardingLocalize("ui.panel.page-onboarding.integration.intro")}
      </p>
      <div class="badges">
        ${e}
        <button @click=${this._createFlow}>
          <action-badge
            clickable
            title=${this.onboardingLocalize("ui.panel.page-onboarding.integration.more_integrations")}
            icon="hass:dots-horizontal"
          ></action-badge>
        </button>
      </div>
      <div class="footer">
        <mwc-button @click=${this._finish}>
          ${this.onboardingLocalize("ui.panel.page-onboarding.integration.finish")}
        </mwc-button>
      </div>
    `}},{kind:"method",key:"firstUpdated",value:function(e){v(w(d.prototype),"firstUpdated",this).call(this,e),(0,c.q)(),this._loadConfigEntries(),r.e(1740).then(r.t.bind(r,61740,23))}},{kind:"method",key:"_createFlow",value:function(){(0,c.t)(this,{dialogClosedCallback:()=>{this._loadConfigEntries(),(0,s.ZJ)(this.hass.connection).refresh()}})}},{kind:"method",key:"_continueFlow",value:function(e){(0,c.t)(this,{continueFlowId:e.currentTarget.flowId,dialogClosedCallback:()=>{this._loadConfigEntries(),(0,s.ZJ)(this.hass.connection).refresh()}})}},{kind:"method",key:"_loadConfigEntries",value:async function(){const e=await(0,a.pB)(this.hass);this._entries=e.filter((e=>!b.has(e.domain)))}},{kind:"method",key:"_finish",value:async function(){(0,i.B)(this,"onboarding-step",{type:"integration"})}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
      .badges {
        margin-top: 24px;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: flex-start;
        align-items: flex-start;
      }
      .badges > * {
        width: 96px;
        margin-bottom: 24px;
      }
      button {
        cursor: pointer;
        padding: 0;
        border: 0;
        background: 0;
        font: inherit;
      }
      .footer {
        text-align: right;
      }
    `}}]}}),n.oi)}}]);
//# sourceMappingURL=chunk.65ed548e0b2fd0391b3c.js.map