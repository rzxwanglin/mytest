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
b_ = function a(a) {
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

Publish =function a(a, c, d, e, f, g) {
            var h;
            h = b_.call(this, "PUBLISH") || this;
            h.topic = a;
            h.payloadMessage = c;
            h.qos = d;
            h.messageIdentifier = e;
            h.retained = f != null ? f : !1;
            h.duplicate = g != null ? g : !1;
            return h
}
mysend_ = function(a, b, c) {
  var e = 3
  a = new (Publish)(a,b,c,e);
  return encode(a)
}

function get_mycode2(message){
    //var message ='{"app_id":"936619743392459","payload":"{\"epoch_id\":7217073016432346726,\"tasks\":[{\"failure_count\":null,\"label\":\"46\",\"payload\":\"{\\\"thread_id\\\":17846712582227458,\\\"otid\\\":\\\"7217072965740846377\\\",\\\"source\\\":65537,\\\"send_type\\\":1,\\\"sync_group\\\":1,\\\"mark_thread_read\\\":1,\\\"text\\\":\\\"c\\\",\\\"initiating_source\\\":1,\\\"skip_url_preview_gen\\\":0,\\\"text_has_links\\\":0,\\\"multitab_env\\\":0}\",\"queue_name\":\"17846712582227458\",\"task_id\":12},{\"failure_count\":null,\"label\":\"21\",\"payload\":\"{\\\"thread_id\\\":17846712582227458,\\\"last_read_watermark_ts\\\":1720684281764,\\\"sync_group\\\":1}\",\"queue_name\":\"17846712582227458\",\"task_id\":13}],\"version_id\":\"7816272465125243\",\"data_trace_id\":\"#mh1JDp0wS92uyj5oTkGKJw\"}","request_id":31,"type":3}'
    var message_ = create(message)
    var mycode = mysend_('/ls_app_settings',message_,1)
    mycode = arrayBufferToBase64(mycode)
    return {'message':message,"code":mycode}
}