/** Pure analytics primitives. Null always means no verified observation. */
export const metricPeriods = {grdp_growth:['2024','2025'],inflation:['2025'],unemployment:['2025-07'],poverty:['2018','2021','2023']};
export const metricLabels = {grdp_growth:'GRDP growth',inflation:'Annual inflation',unemployment:'Unemployment',poverty:'Family poverty'};
export const metricDescriptions={
 grdp_growth:'Real GRDP growth at constant 2018 prices, annual year-on-year change.',
 inflation:'2025 annual average inflation for all-income households. This is not the December rate.',
 unemployment:'July 2025 preliminary unemployment rate, not an annual average.',
 poverty:'Full-year poverty incidence among families from PSA FIES survey waves.'
};
export const periodLabel=p=>p==='2025-07'?'July 2025':p;
export function valueAt(snapshot,region,metric,period){const value=snapshot?.values?.[`${region}|${metric}|${period}`];return typeof value==='number'&&Number.isFinite(value)?value:null;}
export function formatPct(number,digits=1){return number==null?'Not available':`${number.toFixed(digits)}%`;}
export function signedPct(number,digits=1){return number==null?'—':`${number>0?'+':''}${number.toFixed(digits)}%`;}
export function observations(snapshot,metric,period,group='All',search=''){
 const term=search.trim().toLowerCase();
 return (snapshot?.regions||[]).filter(r=>(group==='All'||r.island===group)&&(`${r.name} ${r.short} ${r.code}`).toLowerCase().includes(term)).map(r=>({...r,value:valueAt(snapshot,r.code,metric,period)}));
}
export function rankRegions(rows,sort='desc'){
 return [...rows].sort((a,b)=>a.value==null?1:b.value==null?-1:sort==='asc'?a.value-b.value:b.value-a.value);
}
export function stats(rows){const nums=rows.map(x=>x.value).filter(x=>x!=null);if(!nums.length)return{count:0,min:null,max:null,mean:null};return{count:nums.length,min:Math.min(...nums),max:Math.max(...nums),mean:nums.reduce((a,b)=>a+b,0)/nums.length};}
export function regionTrend(snapshot,metric,code){return (metricPeriods[metric]||[]).map(period=>({period,region:code,value:valueAt(snapshot,code,metric,period)}));}
export function comparisonData(snapshot,metric,codes){return (metricPeriods[metric]||[]).map(period=>({period,...Object.fromEntries(codes.map(code=>[code,valueAt(snapshot,code,metric,period)])),PH:valueAt(snapshot,'PH',metric,period)}));}
export function csvExport(rows,metric,period){const clean=x=>'"'+String(x??'').replaceAll('"','""')+'"';return [['Region','PSGC','Island group','Indicator','Period','Value'].map(clean).join(','),...rows.map(r=>[r.name,r.psgc,r.island,metric,period,r.value??''].map(clean).join(','))].join('\n');}
export function colorFor(value,domain){if(value==null)return '#263540';const [min,max]=domain;const x=max===min?.5:Math.max(0,Math.min(1,(value-min)/(max-min)));const stops=[[30,77,96],[45,135,145],[112,216,191],[211,244,198]];const t=x*3;const i=Math.min(2,Math.floor(t)),f=t-i;return `rgb(${[0,1,2].map(ch=>Math.round(stops[i][ch]*(1-f)+stops[i+1][ch]*f)).join(',')})`;}
