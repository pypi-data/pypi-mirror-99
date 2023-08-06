(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[4608],{44608:(t,e,i)=>{"use strict";i(31206);var a=i(15652),s=i(78956),r=i(50856),n=i(28426),o=i(44583),l=i(1265),d=i(72986),c=i(33367),h=i(21683),p=i(49684);i(10983);let u=null;class f extends((0,c.P)([d.z],n.H3)){static get template(){return r.d`
      <style>
        :host {
          display: block;
        }
        .chartHeader {
          padding: 6px 0 0 0;
          width: 100%;
          display: flex;
          flex-direction: row;
        }
        .chartHeader > div {
          vertical-align: top;
          padding: 0 8px;
        }
        .chartHeader > div.chartTitle {
          padding-top: 8px;
          flex: 0 0 0;
          max-width: 30%;
        }
        .chartHeader > div.chartLegend {
          flex: 1 1;
          min-width: 70%;
        }
        :root {
          user-select: none;
          -moz-user-select: none;
          -webkit-user-select: none;
          -ms-user-select: none;
        }
        .chartTooltip {
          font-size: 90%;
          opacity: 1;
          position: absolute;
          background: rgba(80, 80, 80, 0.9);
          color: white;
          border-radius: 3px;
          pointer-events: none;
          transform: translate(-50%, 12px);
          z-index: 1000;
          width: 200px;
          transition: opacity 0.15s ease-in-out;
        }
        :host([rtl]) .chartTooltip {
          direction: rtl;
        }
        .chartLegend ul,
        .chartTooltip ul {
          display: inline-block;
          padding: 0 0px;
          margin: 5px 0 0 0;
          width: 100%;
        }
        .chartTooltip ul {
          margin: 0 3px;
        }
        .chartTooltip li {
          display: block;
          white-space: pre-line;
        }
        .chartTooltip li::first-line {
          line-height: 0;
        }
        .chartTooltip .title {
          text-align: center;
          font-weight: 500;
        }
        .chartTooltip .beforeBody {
          text-align: center;
          font-weight: 300;
          word-break: break-all;
        }
        .chartLegend li {
          display: inline-block;
          padding: 0 6px;
          max-width: 49%;
          text-overflow: ellipsis;
          white-space: nowrap;
          overflow: hidden;
          box-sizing: border-box;
        }
        .chartLegend li:nth-child(odd):last-of-type {
          /* Make last item take full width if it is odd-numbered. */
          max-width: 100%;
        }
        .chartLegend li[data-hidden] {
          text-decoration: line-through;
        }
        .chartLegend em,
        .chartTooltip em {
          border-radius: 5px;
          display: inline-block;
          height: 10px;
          margin-right: 4px;
          width: 10px;
        }
        :host([rtl]) .chartTooltip em {
          margin-right: inherit;
          margin-left: 4px;
        }
        ha-icon-button {
          color: var(--secondary-text-color);
        }
      </style>
      <template is="dom-if" if="[[unit]]">
        <div class="chartHeader">
          <div class="chartTitle">[[unit]]</div>
          <div class="chartLegend">
            <ul>
              <template is="dom-repeat" items="[[metas]]">
                <li on-click="_legendClick" data-hidden$="[[item.hidden]]">
                  <em style$="background-color:[[item.bgColor]]"></em>
                  [[item.label]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </template>
      <div id="chartTarget" style="height:40px; width:100%">
        <canvas id="chartCanvas"></canvas>
        <div
          class$="chartTooltip [[tooltip.yAlign]]"
          style$="opacity:[[tooltip.opacity]]; top:[[tooltip.top]]; left:[[tooltip.left]]; padding:[[tooltip.yPadding]]px [[tooltip.xPadding]]px"
        >
          <div class="title">[[tooltip.title]]</div>
          <template is="dom-if" if="[[tooltip.beforeBody]]">
            <div class="beforeBody">[[tooltip.beforeBody]]</div>
          </template>
          <div>
            <ul>
              <template is="dom-repeat" items="[[tooltip.lines]]">
                <li>
                  <em style$="background-color:[[item.bgColor]]"></em
                  >[[item.text]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </div>
    `}get chart(){return this._chart}static get properties(){return{data:Object,identifier:String,rendered:{type:Boolean,notify:!0,value:!1,readOnly:!0},metas:{type:Array,value:()=>[]},tooltip:{type:Object,value:()=>({opacity:"0",left:"0",top:"0",xPadding:"5",yPadding:"3"})},unit:Object,rtl:{type:Boolean,reflectToAttribute:!0}}}static get observers(){return["onPropsChange(data)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.onPropsChange(),this._resizeListener=()=>{this._debouncer=s.d.debounce(this._debouncer,h.Wc.after(10),(()=>{this._isAttached&&this.resizeChart()}))},"function"==typeof ResizeObserver?(this.resizeObserver=new ResizeObserver((t=>{t.forEach((()=>{this._resizeListener()}))})),this.resizeObserver.observe(this.$.chartTarget)):this.addEventListener("iron-resize",this._resizeListener),null===u&&(u=Promise.all([i.e(9680),i.e(9109)]).then(i.bind(i,79109))),u.then((t=>{this.ChartClass=t.default,this.onPropsChange()}))}disconnectedCallback(){super.disconnectedCallback(),this._isAttached=!1,this.resizeObserver&&this.resizeObserver.unobserve(this.$.chartTarget),this.removeEventListener("iron-resize",this._resizeListener),void 0!==this._resizeTimer&&(clearInterval(this._resizeTimer),this._resizeTimer=void 0)}onPropsChange(){this._isAttached&&this.ChartClass&&this.data&&this.drawChart()}_customTooltips(t){if(0===t.opacity)return void this.set(["tooltip","opacity"],0);t.yAlign?this.set(["tooltip","yAlign"],t.yAlign):this.set(["tooltip","yAlign"],"no-transform");const e=t.title&&t.title[0]||"";this.set(["tooltip","title"],e),t.beforeBody&&this.set(["tooltip","beforeBody"],t.beforeBody.join("\n"));const i=t.body.map((t=>t.lines));t.body&&this.set(["tooltip","lines"],i.map(((e,i)=>{const a=t.labelColors[i];return{color:a.borderColor,bgColor:a.backgroundColor,text:e.join("\n")}})));const a=this.$.chartTarget.clientWidth;let s=t.caretX;const r=this._chart.canvas.offsetTop+t.caretY;t.caretX+100>a?s=a-100:t.caretX<100&&(s=100),s+=this._chart.canvas.offsetLeft,this.tooltip={...this.tooltip,opacity:1,left:`${s}px`,top:`${r}px`}}_legendClick(t){(t=t||window.event).stopPropagation();let e=t.target||t.srcElement;for(;"LI"!==e.nodeName;)e=e.parentElement;const i=t.model.itemsIndex,a=this._chart.getDatasetMeta(i);a.hidden=null===a.hidden?!this._chart.data.datasets[i].hidden:null,this.set(["metas",i,"hidden"],this._chart.isDatasetVisible(i)?null:"hidden"),this._chart.update()}_drawLegend(){const t=this._chart,e=this._oldIdentifier&&this.identifier===this._oldIdentifier;this._oldIdentifier=this.identifier,this.set("metas",this._chart.data.datasets.map(((i,a)=>({label:i.label,color:i.color,bgColor:i.backgroundColor,hidden:e&&a<this.metas.length?this.metas[a].hidden:!t.isDatasetVisible(a)}))));let i=!1;if(e)for(let e=0;e<this.metas.length;e++){const a=t.getDatasetMeta(e);!!a.hidden!=!!this.metas[e].hidden&&(i=!0),a.hidden=!!this.metas[e].hidden||null}i&&t.update(),this.unit=this.data.unit}_formatTickValue(t,e,i){if(0===i.length)return t;const a=new Date(i[e].value);return(0,p.mr)(a,this.hass.language)}drawChart(){const t=this.data.data,e=this.$.chartCanvas;if(t.datasets&&t.datasets.length||this._chart){if("timeline"!==this.data.type&&t.datasets.length>0){const e=t.datasets.length,i=this.constructor.getColorList(e);for(let a=0;a<e;a++)t.datasets[a].borderColor=i[a].rgbString(),t.datasets[a].backgroundColor=i[a].alpha(.6).rgbaString()}if(this._chart)this._customTooltips({opacity:0}),this._chart.data=t,this._chart.update({duration:0}),this.isTimeline?this._chart.options.scales.yAxes[0].gridLines.display=t.length>1:!0===this.data.legend&&this._drawLegend(),this.resizeChart();else{if(!t.datasets)return;this._customTooltips({opacity:0});const i=[{afterRender:()=>this._setRendered(!0)}];let a={responsive:!0,maintainAspectRatio:!1,animation:{duration:0},hover:{animationDuration:0},responsiveAnimationDuration:0,tooltips:{enabled:!1,custom:this._customTooltips.bind(this)},legend:{display:!1},line:{spanGaps:!0},elements:{font:"12px 'Roboto', 'sans-serif'"},ticks:{fontFamily:"'Roboto', 'sans-serif'"}};a=Chart.helpers.merge(a,this.data.options),a.scales.xAxes[0].ticks.callback=this._formatTickValue.bind(this),"timeline"===this.data.type?(this.set("isTimeline",!0),void 0!==this.data.colors&&(this._colorFunc=this.constructor.getColorGenerator(this.data.colors.staticColors,this.data.colors.staticColorIndex)),void 0!==this._colorFunc&&(a.elements.colorFunction=this._colorFunc),1===t.datasets.length&&(a.scales.yAxes[0].ticks?a.scales.yAxes[0].ticks.display=!1:a.scales.yAxes[0].ticks={display:!1},a.scales.yAxes[0].gridLines?a.scales.yAxes[0].gridLines.display=!1:a.scales.yAxes[0].gridLines={display:!1}),this.$.chartTarget.style.height="50px"):this.$.chartTarget.style.height="160px";const s={type:this.data.type,data:this.data.data,options:a,plugins:i};this._chart=new this.ChartClass(e,s),!0!==this.isTimeline&&!0===this.data.legend&&this._drawLegend(),this.resizeChart()}}}resizeChart(){this._chart&&(void 0!==this._resizeTimer?(clearInterval(this._resizeTimer),this._resizeTimer=void 0,this._resizeChart()):this._resizeTimer=setInterval(this.resizeChart.bind(this),10))}_resizeChart(){const t=this.$.chartTarget,e=this.data.data;if(0===e.datasets.length)return;if(!this.isTimeline)return void this._chart.resize();const i=this._chart.chartArea.top,a=this._chart.chartArea.bottom,s=this._chart.canvas.clientHeight;if(a>0&&(this._axisHeight=s-a+i),!this._axisHeight)return t.style.height="50px",this._chart.resize(),void this.resizeChart();if(this._axisHeight){const i=30*e.datasets.length+this._axisHeight+"px";t.style.height!==i&&(t.style.height=i),this._chart.resize()}}static getColorList(t){let e=!1;t>10&&(e=!0,t=Math.ceil(t/2));const i=360/t,a=[];for(let s=0;s<t;s++)a[s]=Color().hsl(i*s,80,38),e&&(a[s+t]=Color().hsl(i*s,80,62));return a}static getColorGenerator(t,e){const i=["ff0029","66a61e","377eb8","984ea3","00d2d5","ff7f00","af8d00","7f80cd","b3e900","c42e60","a65628","f781bf","8dd3c7","bebada","fb8072","80b1d3","fdb462","fccde5","bc80bd","ffed6f","c4eaff","cf8c00","1b9e77","d95f02","e7298a","e6ab02","a6761d","0097ff","00d067","f43600","4ba93b","5779bb","927acc","97ee3f","bf3947","9f5b00","f48758","8caed6","f2b94f","eff26e","e43872","d9b100","9d7a00","698cff","d9d9d9","00d27e","d06800","009f82","c49200","cbe8ff","fecddf","c27eb6","8cd2ce","c4b8d9","f883b0","a49100","f48800","27d0df","a04a9b"];function a(t){return Color("#"+i[t%i.length])}const s={};let r=0;return e>0&&(r=e),t&&Object.keys(t).forEach((e=>{const i=t[e];isFinite(i)?s[e.toLowerCase()]=a(i):s[e.toLowerCase()]=Color(t[e])})),function(t,e){let i;const n=e[3];if(null===n)return Color().hsl(0,40,38);if(void 0===n)return Color().hsl(120,40,38);let o=n.toLowerCase();return void 0===i&&(e[4]&&(o="on"===o?"off":"off"===o?"on":o),i=s[o]),void 0===i&&(i=a(r),r++,s[o]=i),i}}}customElements.define("ha-chart-base",f);class m extends((0,l.Z)(n.H3)){static get template(){return r.d`
      <style>
        :host {
          display: block;
          overflow: hidden;
          height: 0;
          transition: height 0.3s ease-in-out;
        }
      </style>
      <ha-chart-base
        id="chart"
        hass="[[hass]]"
        data="[[chartData]]"
        identifier="[[identifier]]"
        rendered="{{rendered}}"
      ></ha-chart-base>
    `}static get properties(){return{hass:{type:Object},chartData:Object,data:Object,names:Object,unit:String,identifier:String,isSingleDevice:{type:Boolean,value:!1},endTime:Object,rendered:{type:Boolean,value:!1,observer:"_onRenderedChanged"}}}static get observers(){return["dataChanged(data, endTime, isSingleDevice)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}ready(){super.ready(),this.addEventListener("transitionend",(()=>{this.style.overflow="auto"}))}dataChanged(){this.drawChart()}_onRenderedChanged(t){t&&this.animateHeight()}animateHeight(){requestAnimationFrame((()=>requestAnimationFrame((()=>{this.style.height=this.$.chart.scrollHeight+"px"}))))}drawChart(){if(!this._isAttached)return;const t=this.unit,e=this.data,i=[];let a;if(0===e.length)return;function s(t){const e=parseFloat(t);return isFinite(e)?e:null}a=this.endTime||new Date(Math.max.apply(null,e.map((t=>new Date(t.states[t.states.length-1].last_changed))))),a>new Date&&(a=new Date);const r=this.names||{};e.forEach((e=>{const n=e.domain,o=r[e.entity_id]||e.name;let l;const d=[];function c(t,e){e&&(t>a||(d.forEach(((i,a)=>{null===e[a]&&l&&null!==l[a]&&i.data.push({x:t,y:l[a]}),i.data.push({x:t,y:e[a]})})),l=e))}function h(e,i,a){let s=!1,r=!1;a&&(s="origin"),i&&(r="before"),d.push({label:e,fill:s,steppedLine:r,pointRadius:0,data:[],unitText:t})}if("thermostat"===n||"climate"===n||"water_heater"===n){const t=e.states.some((t=>t.attributes&&t.attributes.hvac_action)),i="climate"===n&&t?t=>"heating"===t.attributes.hvac_action:t=>"heat"===t.state,a="climate"===n&&t?t=>"cooling"===t.attributes.hvac_action:t=>"cool"===t.state,r=e.states.some(i),l=e.states.some(a),d=e.states.some((t=>t.attributes&&t.attributes.target_temp_high!==t.attributes.target_temp_low));h(`${this.hass.localize("ui.card.climate.current_temperature","name",o)}`,!0),r&&h(`${this.hass.localize("ui.card.climate.heating","name",o)}`,!0,!0),l&&h(`${this.hass.localize("ui.card.climate.cooling","name",o)}`,!0,!0),d?(h(`${this.hass.localize("ui.card.climate.target_temperature_mode","name",o,"mode",this.hass.localize("ui.card.climate.high"))}`,!0),h(`${this.hass.localize("ui.card.climate.target_temperature_mode","name",o,"mode",this.hass.localize("ui.card.climate.low"))}`,!0)):h(`${this.hass.localize("ui.card.climate.target_temperature_entity","name",o)}`,!0),e.states.forEach((t=>{if(!t.attributes)return;const e=s(t.attributes.current_temperature),n=[e];if(r&&n.push(i(t)?e:null),l&&n.push(a(t)?e:null),d){const e=s(t.attributes.target_temp_high),i=s(t.attributes.target_temp_low);n.push(e,i),c(new Date(t.last_changed),n)}else{const e=s(t.attributes.temperature);n.push(e),c(new Date(t.last_changed),n)}}))}else if("humidifier"===n)h(`${this.hass.localize("ui.card.humidifier.target_humidity_entity","name",o)}`,!0),h(`${this.hass.localize("ui.card.humidifier.on_entity","name",o)}`,!0,!0),e.states.forEach((t=>{if(!t.attributes)return;const e=s(t.attributes.humidity),i=[e];i.push("on"===t.state?e:null),c(new Date(t.last_changed),i)}));else{h(o,"sensor"===n);let t=null,i=null,a=null;e.states.forEach((e=>{const r=s(e.state),n=new Date(e.last_changed);if(null!==r&&null!==a){const e=n.getTime(),s=a.getTime(),o=i.getTime();c(a,[(s-o)/(e-o)*(r-t)+t]),c(new Date(s+1),[null]),c(n,[r]),i=n,t=r,a=null}else null!==r&&null===a?(c(n,[r]),i=n,t=r):null===r&&null===a&&null!==t&&(a=n)}))}c(a,l),Array.prototype.push.apply(i,d)}));const n={type:"line",unit:t,legend:!this.isSingleDevice,options:{scales:{xAxes:[{type:"time",ticks:{major:{fontStyle:"bold"}}}],yAxes:[{ticks:{maxTicksLimit:7}}]},tooltips:{mode:"neareach",callbacks:{title:(t,e)=>{const i=t[0],a=e.datasets[i.datasetIndex].data[i.index].x;return(0,o.E)(a,this.hass.language)}}},hover:{mode:"neareach"},layout:{padding:{top:5}},elements:{line:{tension:.1,pointRadius:0,borderWidth:1.5},point:{hitRadius:5}},plugins:{filler:{propagate:!0}}},data:{labels:[],datasets:i}};this.chartData=n}}customElements.define("state-history-chart-line",m);var y=i(58831),g=i(87744);const b=new Set(["battery","door","garage_door","gas","lock","opening","problem","safety","smoke","window"]);class v extends((0,l.Z)(n.H3)){static get template(){return r.d`
      <style>
        :host {
          display: block;
          opacity: 0;
          transition: opacity 0.3s ease-in-out;
        }
        :host([rendered]) {
          opacity: 1;
        }

        ha-chart-base {
          direction: ltr;
        }
      </style>
      <ha-chart-base
        hass="[[hass]]"
        data="[[chartData]]"
        rendered="{{rendered}}"
        rtl="{{rtl}}"
      ></ha-chart-base>
    `}static get properties(){return{hass:{type:Object},chartData:Object,data:{type:Object,observer:"dataChanged"},names:Object,noSingle:Boolean,endTime:Date,rendered:{type:Boolean,value:!1,reflectToAttribute:!0},rtl:{reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}static get observers(){return["dataChanged(data, endTime, localize, language)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}dataChanged(){this.drawChart()}drawChart(){let t=this.data;if(!this._isAttached)return;t||(t=[]);const e=new Date(t.reduce(((t,e)=>Math.min(t,new Date(e.data[0].last_changed))),new Date));let i=this.endTime||new Date(t.reduce(((t,e)=>Math.max(t,new Date(e.data[e.data.length-1].last_changed))),e));i>new Date&&(i=new Date);const a=[],s=[],r=this.names||{};t.forEach((t=>{let n,o=null,l=null,d=e;const c=r[t.entity_id]||t.name,h="binary_sensor"===(0,y.M)(t.entity_id)&&b.has(this.hass.states[t.entity_id].attributes.device_class),p=[];t.data.forEach((t=>{let e=t.state;void 0!==e&&""!==e||(e=null),new Date(t.last_changed)>i||(null!==o&&e!==o?(n=new Date(t.last_changed),p.push([d,n,l,o,h]),o=e,l=t.state_localize,d=n):null===o&&(o=e,l=t.state_localize,d=new Date(t.last_changed)))})),null!==o&&p.push([d,i,l,o,h]),s.push({data:p,entity_id:t.entity_id}),a.push(c)}));const n={type:"timeline",options:{tooltips:{callbacks:{label:(t,e)=>{const i=e.datasets[t.datasetIndex].data[t.index],a=(0,o.E)(i[0],this.hass.language),s=(0,o.E)(i[1],this.hass.language);return[i[2],a,s]},beforeBody:(t,e)=>{if(!this.hass.userData||!this.hass.userData.showAdvanced||!t[0])return"";return e.datasets[t[0].datasetIndex].entity_id||""}}},scales:{xAxes:[{ticks:{major:{fontStyle:"bold"}}}],yAxes:[{afterSetDimensions:t=>{t.maxWidth=.18*t.chart.width},position:this._computeRTL?"right":"left"}]}},data:{labels:a,datasets:s},colors:{staticColors:{on:1,off:0,home:1,not_home:0,unavailable:"#a0a0a0",unknown:"#606060",idle:2},staticColorIndex:3}};this.chartData=n}_computeRTL(t){return(0,g.HE)(t)}}customElements.define("state-history-chart-timeline",v);var _=i(7323);function w(){w=function(){return t};var t={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(t,e){["method","field"].forEach((function(i){e.forEach((function(e){e.kind===i&&"own"===e.placement&&this.defineClassElement(t,e)}),this)}),this)},initializeClassElements:function(t,e){var i=t.prototype;["method","field"].forEach((function(a){e.forEach((function(e){var s=e.placement;if(e.kind===a&&("static"===s||"prototype"===s)){var r="static"===s?t:i;this.defineClassElement(r,e)}}),this)}),this)},defineClassElement:function(t,e){var i=e.descriptor;if("field"===e.kind){var a=e.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===a?void 0:a.call(t)}}Object.defineProperty(t,e.key,i)},decorateClass:function(t,e){var i=[],a=[],s={static:[],prototype:[],own:[]};if(t.forEach((function(t){this.addElementPlacement(t,s)}),this),t.forEach((function(t){if(!C(t))return i.push(t);var e=this.decorateElement(t,s);i.push(e.element),i.push.apply(i,e.extras),a.push.apply(a,e.finishers)}),this),!e)return{elements:i,finishers:a};var r=this.decorateConstructor(i,e);return a.push.apply(a,r.finishers),r.finishers=a,r},addElementPlacement:function(t,e,i){var a=e[t.placement];if(!i&&-1!==a.indexOf(t.key))throw new TypeError("Duplicated element ("+t.key+")");a.push(t.key)},decorateElement:function(t,e){for(var i=[],a=[],s=t.decorators,r=s.length-1;r>=0;r--){var n=e[t.placement];n.splice(n.indexOf(t.key),1);var o=this.fromElementDescriptor(t),l=this.toElementFinisherExtras((0,s[r])(o)||o);t=l.element,this.addElementPlacement(t,e),l.finisher&&a.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],e);i.push.apply(i,d)}}return{element:t,finishers:a,extras:i}},decorateConstructor:function(t,e){for(var i=[],a=e.length-1;a>=0;a--){var s=this.fromClassDescriptor(t),r=this.toClassDescriptor((0,e[a])(s)||s);if(void 0!==r.finisher&&i.push(r.finisher),void 0!==r.elements){t=r.elements;for(var n=0;n<t.length-1;n++)for(var o=n+1;o<t.length;o++)if(t[n].key===t[o].key&&t[n].placement===t[o].placement)throw new TypeError("Duplicated element ("+t[n].key+")")}}return{elements:t,finishers:i}},fromElementDescriptor:function(t){var e={kind:t.kind,key:t.key,placement:t.placement,descriptor:t.descriptor};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===t.kind&&(e.initializer=t.initializer),e},toElementDescriptors:function(t){var e;if(void 0!==t)return(e=t,function(t){if(Array.isArray(t))return t}(e)||function(t){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(t))return Array.from(t)}(e)||function(t,e){if(t){if("string"==typeof t)return E(t,e);var i=Object.prototype.toString.call(t).slice(8,-1);return"Object"===i&&t.constructor&&(i=t.constructor.name),"Map"===i||"Set"===i?Array.from(t):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?E(t,e):void 0}}(e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(t){var e=this.toElementDescriptor(t);return this.disallowProperty(t,"finisher","An element descriptor"),this.disallowProperty(t,"extras","An element descriptor"),e}),this)},toElementDescriptor:function(t){var e=String(t.kind);if("method"!==e&&"field"!==e)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+e+'"');var i=z(t.key),a=String(t.placement);if("static"!==a&&"prototype"!==a&&"own"!==a)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+a+'"');var s=t.descriptor;this.disallowProperty(t,"elements","An element descriptor");var r={kind:e,key:i,placement:a,descriptor:Object.assign({},s)};return"field"!==e?this.disallowProperty(t,"initializer","A method descriptor"):(this.disallowProperty(s,"get","The property descriptor of a field descriptor"),this.disallowProperty(s,"set","The property descriptor of a field descriptor"),this.disallowProperty(s,"value","The property descriptor of a field descriptor"),r.initializer=t.initializer),r},toElementFinisherExtras:function(t){return{element:this.toElementDescriptor(t),finisher:D(t,"finisher"),extras:this.toElementDescriptors(t.extras)}},fromClassDescriptor:function(t){var e={kind:"class",elements:t.map(this.fromElementDescriptor,this)};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),e},toClassDescriptor:function(t){var e=String(t.kind);if("class"!==e)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+e+'"');this.disallowProperty(t,"key","A class descriptor"),this.disallowProperty(t,"placement","A class descriptor"),this.disallowProperty(t,"descriptor","A class descriptor"),this.disallowProperty(t,"initializer","A class descriptor"),this.disallowProperty(t,"extras","A class descriptor");var i=D(t,"finisher");return{elements:this.toElementDescriptors(t.elements),finisher:i}},runClassFinishers:function(t,e){for(var i=0;i<e.length;i++){var a=(0,e[i])(t);if(void 0!==a){if("function"!=typeof a)throw new TypeError("Finishers must return a constructor.");t=a}}return t},disallowProperty:function(t,e,i){if(void 0!==t[e])throw new TypeError(i+" can't have a ."+e+" property.")}};return t}function k(t){var e,i=z(t.key);"method"===t.kind?e={value:t.value,writable:!0,configurable:!0,enumerable:!1}:"get"===t.kind?e={get:t.value,configurable:!0,enumerable:!1}:"set"===t.kind?e={set:t.value,configurable:!0,enumerable:!1}:"field"===t.kind&&(e={configurable:!0,writable:!0,enumerable:!0});var a={kind:"field"===t.kind?"field":"method",key:i,placement:t.static?"static":"field"===t.kind?"own":"prototype",descriptor:e};return t.decorators&&(a.decorators=t.decorators),"field"===t.kind&&(a.initializer=t.value),a}function x(t,e){void 0!==t.descriptor.get?e.descriptor.get=t.descriptor.get:e.descriptor.set=t.descriptor.set}function C(t){return t.decorators&&t.decorators.length}function T(t){return void 0!==t&&!(void 0===t.value&&void 0===t.writable)}function D(t,e){var i=t[e];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+e+"' to be a function");return i}function z(t){var e=function(t,e){if("object"!=typeof t||null===t)return t;var i=t[Symbol.toPrimitive];if(void 0!==i){var a=i.call(t,e||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(t)}(t,"string");return"symbol"==typeof e?e:String(e)}function E(t,e){(null==e||e>t.length)&&(e=t.length);for(var i=0,a=new Array(e);i<e;i++)a[i]=t[i];return a}!function(t,e,i,a){var s=w();if(a)for(var r=0;r<a.length;r++)s=a[r](s);var n=e((function(t){s.initializeInstanceElements(t,o.elements)}),i),o=s.decorateClass(function(t){for(var e=[],i=function(t){return"method"===t.kind&&t.key===r.key&&t.placement===r.placement},a=0;a<t.length;a++){var s,r=t[a];if("method"===r.kind&&(s=e.find(i)))if(T(r.descriptor)||T(s.descriptor)){if(C(r)||C(s))throw new ReferenceError("Duplicated methods ("+r.key+") can't be decorated.");s.descriptor=r.descriptor}else{if(C(r)){if(C(s))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+r.key+").");s.decorators=r.decorators}x(r,s)}else e.push(r)}return e}(n.d.map(k)),t);s.initializeClassElements(n.F,o.elements),s.runClassFinishers(n.F,o.finishers)}([(0,a.Mo)("state-history-charts")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"historyData",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"names",value:()=>!1},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"endTime",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"upToNow",value:()=>!1},{kind:"field",decorators:[(0,a.Cb)({type:Boolean,attribute:"no-single"})],key:"noSingle",value:()=>!1},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"isLoadingData",value:()=>!1},{kind:"method",key:"render",value:function(){if(!(0,_.p)(this.hass,"history"))return a.dy` <div class="info">
        ${this.hass.localize("ui.components.history_charts.history_disabled")}
      </div>`;if(this.isLoadingData&&!this.historyData)return a.dy` <div class="info">
        ${this.hass.localize("ui.components.history_charts.loading_history")}
      </div>`;if(this._isHistoryEmpty())return a.dy` <div class="info">
        ${this.hass.localize("ui.components.history_charts.no_history_found")}
      </div>`;const t=this.upToNow?new Date:this.endTime||new Date;return a.dy`
      ${this.historyData.timeline.length?a.dy`
            <state-history-chart-timeline
              .hass=${this.hass}
              .data=${this.historyData.timeline}
              .endTime=${t}
              .noSingle=${this.noSingle}
              .names=${this.names}
            ></state-history-chart-timeline>
          `:a.dy``}
      ${this.historyData.line.map((e=>a.dy`
          <state-history-chart-line
            .hass=${this.hass}
            .unit=${e.unit}
            .data=${e.data}
            .identifier=${e.identifier}
            .isSingleDevice=${!this.noSingle&&e.data&&1===e.data.length}
            .endTime=${t}
            .names=${this.names}
          ></state-history-chart-line>
        `))}
    `}},{kind:"method",key:"shouldUpdate",value:function(t){return!(1===t.size&&t.has("hass"))}},{kind:"method",key:"_isHistoryEmpty",value:function(){const t=!this.historyData||!this.historyData.timeline||!this.historyData.line||0===this.historyData.timeline.length&&0===this.historyData.line.length;return!this.isLoadingData&&t}},{kind:"get",static:!0,key:"styles",value:function(){return a.iv`
      :host {
        display: block;
        /* height of single timeline chart = 58px */
        min-height: 58px;
      }
      .info {
        text-align: center;
        line-height: 58px;
        color: var(--secondary-text-color);
      }
    `}}]}}),a.oi)},1265:(t,e,i)=>{"use strict";i.d(e,{Z:()=>a});const a=(0,i(76389).o)((t=>class extends t{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(t){return t}}))}}]);
//# sourceMappingURL=chunk.93853f5cd073c3d2502e.js.map