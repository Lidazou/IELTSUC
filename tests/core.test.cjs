const {test}=require('node:test'),assert=require('node:assert/strict');
const {parseWords,splitTime,grade}=require('../core.cjs');
test('OCR columns preserve English POS and Chinese',()=>{assert.deepEqual(parseWords('sustainable\tadj.\t可持续的\ncritical thinking  n. 批判性思维'),[{english:'sustainable',pos:'adj.',translation:'可持续的'},{english:'critical thinking',pos:'n.',translation:'批判性思维'}])});
test('cross midnight time belongs to each calendar day',()=>{let s=new Date(2026,9,28,23,59,50).getTime(),e=new Date(2026,9,29,0,0,10).getTime();assert.deepEqual(splitTime(s,e),[{date:'2026-10-28',seconds:10},{date:'2026-10-29',seconds:10}])});
test('answer matching accepts alternatives without accepting partial words',()=>{let r=grade([{answer:['three','3']},{answer:'carbon'}],[' 3 ','car']);assert.equal(r[0].correct,true);assert.equal(r[1].correct,false)});
