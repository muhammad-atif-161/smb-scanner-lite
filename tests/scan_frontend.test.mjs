import test from "node:test";
import assert from "node:assert/strict";
import { checkedOrigin, makeScanClient, parseSession, ScanAPIError } from "../website/scan-app.mjs";

const apiOrigin="https://smbscanner-edge.example.workers.dev";
const id="123e4567-e89b-12d3-a456-426614174000";
const token="a".repeat(64);

test("API URL must be a strict HTTPS origin",()=>{
  assert.equal(checkedOrigin(apiOrigin),apiOrigin);
  for(const bad of ["","http://api.example.com","https://api.example.com/steal",
     "https://x:y@api.example.com","https://api.example.com:8443",
     "https://api.example.com/?token=x","https://api.example.com/#token",
     "javascript:alert(1)"]){
    assert.throws(()=>checkedOrigin(bad),undefined,bad);
  }
});

test("create sends only specified public fields, never scanner credentials",async()=>{
  const calls=[];
  const client=makeScanClient(apiOrigin,async(url,options)=>{
    calls.push({url,options});
    return Response.json({assessment_id:id,access_token:token,dns_record_name:"_verify.domain.test"});
  });
  const result=await client.create({name:"Tester",email:"owner@example.com",domain:"valid.com",note:"private"});
  assert.equal(result.assessment_id,id);
  assert.equal(calls.length,1);
  assert.equal(calls[0].url,apiOrigin+"/api/v1/assessments");
  assert.equal(calls[0].options.method,"POST");
  assert.equal(calls[0].options.headers.Authorization,undefined);
  assert.deepEqual(JSON.parse(calls[0].options.body),{name:"Tester",email:"owner@example.com",domain:"valid.com"});
  assert.equal(calls[0].options.credentials,"omit");
  assert.equal(calls[0].options.referrerPolicy,"no-referrer");
});

test("owner token used as header, not URL/query, for verify/status/preview",async()=>{
  const calls=[];
  const client=makeScanClient(apiOrigin,async(url,options)=>{
    calls.push({url,options});
    return Response.json({status:"verified"});
  });
  await client.verify(id,token);
  await client.status(id,token);
  await client.preview(id,token);
  assert.deepEqual(calls.map(x=>x.options.method),["POST","GET","GET"]);
  assert.ok(calls.every(x=>x.options.headers.Authorization==="Bearer "+token));
  assert.ok(calls.every(x=>!x.url.includes(token)));
  assert.ok(calls.every(x=>!x.options.headers["Content-Type"]));
  assert.ok(calls.every(x=>x.options.redirect==="error"));
});

test("dispatch is one POST and has no built-in network retry",async()=>{
  let attempts=0;
  const client=makeScanClient(apiOrigin,async()=>{
    attempts++;
    throw new Error("ambiguous network failure");
  });
  await assert.rejects(client.dispatch(id,token),
    e=>e instanceof ScanAPIError && e.status===0 && /Check assessment status/.test(e.message));
  assert.equal(attempts,1);
});

test("backend error messages returned safely and do not contain raw report content",async()=>{
  const client=makeScanClient(apiOrigin,async()=>new Response(JSON.stringify({error:"Assessments are disabled"}),{
    status:503,headers:{"Content-Type":"application/json"},
  }));
  await assert.rejects(client.create({name:"A",email:"a@b.com",domain:"c.com"}),
    e=>e.status===503 && e.message==="Assessments are disabled");
});

test("invalid IDs, tokens, and recovery sessions rejected before network",async()=>{
  let network=0;
  const client=makeScanClient(apiOrigin,async()=>{
    network++;
    return Response.json({});
  });
  assert.throws(()=>client.status("../secret",token));
  await assert.rejects(client.status(id,"not-a-token"));
  assert.equal(network,0);
  assert.equal(parseSession('{"id":"evil"}'),null);
  assert.equal(parseSession("not-json"),null);
  const valid=parseSession({id,token,domain:"owned.example.com",
    recordName:"_smbscanner-verify.owned.example.com",recordValue:"smbscanner-verification=xyz"});
  assert.equal(valid.id,id);
  assert.equal(valid.token,token);
});

test("tier Formspree notification never includes credentials or assessment tokens",async()=>{
  const {notifyRequest,checkedFormEndpoint}=await import("../website/scan-app.mjs");
  const calls=[];
  await notifyRequest("https://formspree.io/f/xbggayev",
    {name:"A",email:"a@example.org",domain:"owned.example.org",tier:"deep",authorised:true,
     token:"secret",recordValue:"secret",assessmentId:"secret"},
    async(url,options)=>{calls.push({url,options});return Response.json({ok:true})});
  assert.equal(calls.length,1);
  assert.equal(checkedFormEndpoint(calls[0].url),"https://formspree.io/f/xbggayev");
  assert.deepEqual(Object.keys(JSON.parse(calls[0].options.body)).sort(),
    ["authorised","domain","email","kind","name","note","page","tier"].sort());
  assert.equal(JSON.parse(calls[0].options.body).tier,"deep");
  assert.equal(calls[0].options.credentials,"omit");
  assert.throws(()=>checkedFormEndpoint("https://other-site.test/f/xbggayev"));
});


test("full evidence is requested only with a private owner bearer; checkout has no card fields",async()=>{
  const calls=[];
  const client=makeScanClient(apiOrigin,async(url,options)=>{
    calls.push({url,options});
    return Response.json(options.method==="POST"
      ? {checkout_url:"https://checkout.stripe.com/c/pay/cs_test_demo"}
      : {report:{report_id:"R1",target:"owned.example.org",results:[]}});
  });
  const checkout=await client.checkout(id,token);
  const full=await client.report(id,token);
  assert.match(checkout.checkout_url,/checkout\.stripe\.com/);
  assert.equal(full.report.report_id,"R1");
  assert.deepEqual(calls.map(x=>x.options.method),["POST","GET"]);
  assert.deepEqual(calls.map(x=>new URL(x.url).pathname),
    ["/api/v1/assessments/"+id+"/checkout","/api/v1/assessments/"+id+"/report"]);
  assert.ok(calls.every(x=>x.options.headers.Authorization==="Bearer "+token));
  assert.ok(calls.every(x=>!x.url.includes(token)));
  assert.ok(calls.every(x=>x.options.credentials==="omit"));
  assert.ok(calls.every(x=>x.options.body===undefined));
});
test("Stripe hosted checkout URL is strictly validated against redirect injection",async()=>{
  const {checkedCheckoutUrl}=await import("../website/scan-app.mjs");
  assert.equal(checkedCheckoutUrl("https://checkout.stripe.com/c/pay/cs_test_123"),
    "https://checkout.stripe.com/c/pay/cs_test_123");
  for(const value of ["","javascript:alert(1)",
    "http://checkout.stripe.com/c/pay/cs_test_123",
    "https://checkout.stripe.com.evil.test/pay",
    "https://evil.test/pay","https://checkout.stripe.com@evil.test/pay",
    "https://checkout.stripe.com:8443/pay",
    "https://checkout.stripe.com/pay#private"]) {
    assert.throws(()=>checkedCheckoutUrl(value),undefined,value);
  }
});
test("a backend 402 is not interpreted as a successful payment",async()=>{
  const client=makeScanClient(apiOrigin,async()=>Response.json(
    {error:"Full evidence report requires verified $19 payment"},{status:402}));
  await assert.rejects(client.report(id,token),
    e=>e instanceof ScanAPIError && e.status===402);
});
