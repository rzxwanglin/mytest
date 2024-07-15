UTF8Length = function f(a) {
    var b = 0;
    for (var c = 0, d = a.length; c < d; c++) {
        var e = a.charCodeAt(c);
        e < 128 ? b += 1 : e < 2048 ? b += 2 : e >= 55296 && e <= 56319 ? (b += 4,
        c++) : b += 3
    }
    return b
}

convertStringToUTF8 = function j(a, b, c) {
    c = c;
    for (var d = 0, e = a.length; d < e; d++) {
        var f = a.charCodeAt(d);
        f < 128 ? b[c++] = f : f < 2048 ? (b[c++] = 192 | f >> 6,
        b[c++] = 128 | f & 63) : f < 55296 || f >= 57344 ? (b[c++] = 224 | f >> 12,
        b[c++] = 128 | f >> 6 & 63,
        b[c++] = 128 | f & 63) : (f = 65536 + ((f & 1023) << 10 | a.charCodeAt(++d) & 1023),
        b[c++] = 240 | f >> 18,
        b[c++] = 128 | f >> 12 & 63,
        b[c++] = 128 | f >> 6 & 63,
        b[c++] = 128 | f & 63)
    }
}
a_=  function a(a, b) {
            this.payloadString = a,
            this.payloadBytes = b
}

create = function(b) {
    var c = new Uint8Array(new ArrayBuffer(UTF8Length(b)));
    convertStringToUTF8(b, c, 0);
    return new a_(b,c)
} 


coinflip = function b(b) {
                return a.apply(this, arguments)
            }
scheduleLoggingCallback= function(a) {
            return this.$9 != null ? this.$9(a) : a()
        }

b = function a(a) {
            h ={
              "CONNECT": 1,
              "CONNACK": 2,
              "PUBLISH": 3,
              "PUBACK": 4,
              "SUBSCRIBE": 8,
              "SUBACK": 9,
              "UNSUBSCRIBE": 10,
              "UNSUBACK": 11,
              "PINGREQ": 12,
              "PINGRESP": 13,
              "DISCONNECT": 14
          }
           this.messageType = h[a]
}
Publish = function (a, c, d, e, f, g) {
            var h;
            h = b.call(this, "PUBLISH") || this;
            h.topic = a;
            h.payloadMessage = c;
            h.qos = d;
            h.messageIdentifier = e;
            h.retained = f != null ? f : !1;
            h.duplicate = g != null ? g : !1;
            return h
}
encodeMultiByteInt=    function (a) {
        a = a;
        var b = new Array(1);
        for (var c = 0; c < 4; c++) {
            var d = a % 128;
            a >>= 7;
            if (a > 0)
                b[c] = d | 128;
            else {
                b[c] = d;
                break
            }
        }
        return b
    }

    

writeString=   function (a, b, c, d) {
        function h(a, b, c) {
            c = c;
            b[c++] = a >> 8;
            b[c++] = a % 256;
            return c
        }
        function j(a, b, c) {
        c = c;
        for (var d = 0, e = a.length; d < e; d++) {
            var f = a.charCodeAt(d);
            f < 128 ? b[c++] = f : f < 2048 ? (b[c++] = 192 | f >> 6,
            b[c++] = 128 | f & 63) : f < 55296 || f >= 57344 ? (b[c++] = 224 | f >> 12,
            b[c++] = 128 | f >> 6 & 63,
            b[c++] = 128 | f & 63) : (f = 65536 + ((f & 1023) << 10 | a.charCodeAt(++d) & 1023),
            b[c++] = 240 | f >> 18,
            b[c++] = 128 | f >> 12 & 63,
            b[c++] = 128 | f >> 6 & 63,
            b[c++] = 128 | f & 63)
        }
    }
        d = h(b, c, d);
        j(a, c, d);
        return d + b
    }
writeUInt16BE= function h(a, b, c) {
        c = c;
        b[c++] = a >> 8;
        b[c++] = a % 256;
        return c
    }

encode = function(mythis) {
            var a = (mythis.messageType & 15) << 4;
            mythis.duplicate && (a |= 8);
            a = a |= mythis.qos << 1;
            mythis.retained && a != 1;
            var b = UTF8Length(mythis.topic)
              , c = b + 2
              , e = mythis.qos === 0 ? 0 : 2;
            c += e;
            e = mythis.payloadMessage.payloadBytes;
            c += e.byteLength;
            var f = encodeMultiByteInt(c);
            c = new ArrayBuffer(1 + f.length + c);
            var g = new Uint8Array(c);
            g[0] = a;
            g.set(f, 1);
            a = 1 + f.length;
            a = writeString(mythis.topic, b, g, a);
            mythis.qos !== 0 && mythis.messageIdentifier != null && (a = writeUInt16BE(mythis.messageIdentifier, g, a));
            g.set(e, a);
            return c
}


mysend_ = function(a, b, c) {
  var e = 3
  a = new (Publish)(a,b,c,e);
  return encode(a)
}


function arrayBufferToBase64(buffer) {
    const binary = new Uint8Array(buffer).reduce((data, byte) => data + String.fromCharCode(byte), '');
    return Buffer.from(binary, 'binary').toString('base64');
}


function get_mycode2(req_mes,message){
    //var message ='{"app_id":"936619743392459","payload":"{\"epoch_id\":7217073016432346726,\"tasks\":[{\"failure_count\":null,\"label\":\"46\",\"payload\":\"{\\\"thread_id\\\":17846712582227458,\\\"otid\\\":\\\"7217072965740846377\\\",\\\"source\\\":65537,\\\"send_type\\\":1,\\\"sync_group\\\":1,\\\"mark_thread_read\\\":1,\\\"text\\\":\\\"c\\\",\\\"initiating_source\\\":1,\\\"skip_url_preview_gen\\\":0,\\\"text_has_links\\\":0,\\\"multitab_env\\\":0}\",\"queue_name\":\"17846712582227458\",\"task_id\":12},{\"failure_count\":null,\"label\":\"21\",\"payload\":\"{\\\"thread_id\\\":17846712582227458,\\\"last_read_watermark_ts\\\":1720684281764,\\\"sync_group\\\":1}\",\"queue_name\":\"17846712582227458\",\"task_id\":13}],\"version_id\":\"7816272465125243\",\"data_trace_id\":\"#mh1JDp0wS92uyj5oTkGKJw\"}","request_id":31,"type":3}'
    var message_ = create(message)
    var mycode = mysend_(req_mes,message_,1)
    mycode = arrayBufferToBase64(mycode)
    return {'message':message,"code":mycode}
}

function get_mycode3(topic,messageIdentifier){
    encode3 = function(mythis) {
            var a = 128
            a |= 2;
            var b =UTF8Length(mythis.topic) //20
              , c = 2 + b + 2;
            mythis.messageType ===8 && (c += 1);
            var e = encodeMultiByteInt(c);
            c = new ArrayBuffer(1 + e.length + c);
            var f = new Uint8Array(c);
            f[0] = a;
            a = 1;
            f.set(e, 1);
            a += e.length;
            mythis.messageIdentifier != null && (a = writeUInt16BE(mythis.messageIdentifier, f, a));
            a = writeString(mythis.topic, b, f, a);
            mythis.messageType === 8 && mythis.qos != null && (f[a++] = mythis.qos);
            return c
        }
    //var message ='{"app_id":"936619743392459","payload":"{\"epoch_id\":7217073016432346726,\"tasks\":[{\"failure_count\":null,\"label\":\"46\",\"payload\":\"{\\\"thread_id\\\":17846712582227458,\\\"otid\\\":\\\"7217072965740846377\\\",\\\"source\\\":65537,\\\"send_type\\\":1,\\\"sync_group\\\":1,\\\"mark_thread_read\\\":1,\\\"text\\\":\\\"c\\\",\\\"initiating_source\\\":1,\\\"skip_url_preview_gen\\\":0,\\\"text_has_links\\\":0,\\\"multitab_env\\\":0}\",\"queue_name\":\"17846712582227458\",\"task_id\":12},{\"failure_count\":null,\"label\":\"21\",\"payload\":\"{\\\"thread_id\\\":17846712582227458,\\\"last_read_watermark_ts\\\":1720684281764,\\\"sync_group\\\":1}\",\"queue_name\":\"17846712582227458\",\"task_id\":13}],\"version_id\":\"7816272465125243\",\"data_trace_id\":\"#mh1JDp0wS92uyj5oTkGKJw\"}","request_id":31,"type":3}'
    message_ ={
        "messageIdentifier":messageIdentifier, //3
        "messageType": 8,
        //"topic":"/ls_foreground_state",
        "topic":topic,
        "qos":0
    }
    var mycode = encode3(message_)
    mycode = arrayBufferToBase64(mycode)
    return {'message':message_,"code":mycode}
}




function get_mycode4(topic,messageIdentifier){
      encode4 = function(mythis) {
    // {messageType: 12}
            var a = new ArrayBuffer(2)
              , b = new Uint8Array(a);
            b[0] = (mythis.messageType & 15) << 4;
            return a
        }
    message_ ={
        messageType: 12
    }
    var mycode = encode4(message_)
    mycode = arrayBufferToBase64(mycode)
    return {'message':message_,"code":mycode}
}

//"{"a":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","aid":936619743392459,"aids":null,"chat_on":true,"cp":3,"ct":"cookie_auth","d":"233cdf9f-adb1-40fd-ac2c-959748663ada","dc":"","ecp":10,"fg":false,"gas":null,"mqtt_sid":"","no_auto_fg":true,"p":null,"pack":[],"php_override":"","pm":[{"isBase64Publish":false,"messageId":65536,"payload":"{\"ls_fdid\":\"\",\"ls_sv\":\"8255578237827838\"}","qos":1,"topic":"/ls_app_settings"}],"s":3864044398182399,"st":["/ls_foreground_state","/ls_resp","/pubsub"],"u":"17841466750442299"}"